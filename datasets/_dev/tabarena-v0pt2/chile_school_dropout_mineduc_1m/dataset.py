"""Curated dataset definition for `chile_school_dropout_mineduc_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

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
    decode,
    drop_columns,
)

# The school years whose students are the rows (year t); the label reads the file of t + 1, the history that of t - 1.
YEARS = tuple(range(2018, 2025))
# One folder per yearly RAR archive (unpacked), each holding one semicolon-separated CSV.
YEAR_FOLDERS = {
    2017: "Rendimiento-2017",
    2018: "Rendimiento-2018",
    2019: "Rendimiento-2019",
    2020: "Rendimiento-2020",
    2021: "Rendimiento-2021",
    2022: "Rendimiento-2022",
    2023: "Rendimiento-2023",
    2024: "Rendimiento_2024",
    2025: "Rendimiento-por-estudiante-2025",
}
PREPARED = "student_years.parquet"

# The grouped teaching levels (COD_ENSE2, Anexo III of the record layout).
CHILD_YOUTH = (2, 5, 7)  # basic for children; secondary scientific-humanistic, and TP or artistic, for youth
SECONDARY_YOUTH = (5, 7)
ADULT = (3, 6, 8)  # basic, scientific-humanistic, and TP or artistic education for adults
SPECIAL = 4  # special education, in the files from 2023 on
# The order in which a student's non-transfer rows of one year are taken when picking the final one.
STATUS_ORDER = {"P": 0, "R": 1, "Y": 2}

# The re-link of a changed student id: an absent student of year t and an id new in t + 1 match on the school, the
# birth month, the sex and the home commune, at the same grade level or the next one (grade levels 1 to 12).
LINK_KEYS = ("rbd", "fec_nac_alu", "gen_alu", "cod_com_alu")
PLACEHOLDER_BIRTH_MONTH = "190001"

# The columns of the yearly files the task reads (the file headers differ in case between years); the TP mention
# (COD_MEN) is in the files from 2019 on.
OPTIONAL_INT_COLUMNS = ("cod_men",)
TEXT_COLUMNS = ("let_cur", "fec_nac_alu", "sit_fin_r")
DECIMAL_COLUMNS = ("prom_gral", "asistencia")
INT_COLUMNS = (
    "mrun",
    "rbd",
    "cod_reg_rbd",
    "cod_com_rbd",
    "cod_depe",
    "rural_rbd",
    "cod_ense",
    "cod_ense2",
    "cod_grado",
    "cod_jor",
    "cod_tip_cur",
    "cod_des_cur",
    "gen_alu",
    "edad_alu",
    "cod_reg_alu",
    "cod_com_alu",
    "cod_sec",
    "cod_espe",
)
COLUMNS = INT_COLUMNS + OPTIONAL_INT_COLUMNS + TEXT_COLUMNS + DECIMAL_COLUMNS

# The codebook's words for its codes (record layout "Esquema de registro bases de Rendimiento escolar 2002-2023 por
# estudiante", Centro de Estudios Mineduc; Anexos I to III), in English.
REGIONS = {
    1: "Tarapaca",
    2: "Antofagasta",
    3: "Atacama",
    4: "Coquimbo",
    5: "Valparaiso",
    6: "O'Higgins",
    7: "Maule",
    8: "Biobio",
    9: "Araucania",
    10: "Los Lagos",
    11: "Aysen",
    12: "Magallanes",
    13: "Metropolitana",
    14: "Los Rios",
    15: "Arica y Parinacota",
    16: "Nuble",
}
STATUS = {"P": "promoted", "R": "failed", "Y": "withdrawn"}
# Anexo VI: the economic sectors and specialties of TP and artistic secondary (0 is the general cycle of 1st and 2nd
# secondary, or no information; never 0 in TP 3rd and 4th secondary on the rows).
TP_SECTORS = {
    0: "general cycle or not applicable",
    410: "administration and commerce",
    510: "construction",
    520: "metalworking",
    530: "electricity",
    540: "mining",
    550: "graphics",
    560: "chemistry",
    570: "clothing",
    580: "technology and telecommunications",
    610: "food",
    620: "social programmes and projects",
    630: "hotels and tourism",
    640: "health and education",
    710: "timber",
    720: "agriculture and livestock",
    810: "maritime",
    910: "visual arts",
    920: "performing arts, theatre",
    930: "performing arts, dance",
}
TP_SPECIALTIES = {
    0: "general cycle or not applicable",
    41001: "administration",
    41002: "accounting",
    41003: "secretarial work",
    41004: "sales",
    41005: "administration (with mention)",
    51001: "building",
    51002: "construction finishing",
    51003: "industrial assembly",
    51004: "roads and infrastructure",
    51005: "plumbing installations",
    51006: "refrigeration and air conditioning",
    51008: "plumbing installations (51008)",
    51009: "construction (with mention)",
    52008: "industrial mechanics",
    52009: "metal structures",
    52010: "automotive mechanics",
    52011: "die making",
    52012: "aircraft maintenance mechanics",
    52013: "industrial mechanics (with mention)",
    53014: "electricity",
    53015: "electronics",
    53016: "telecommunications (53016)",
    54018: "mining",
    54019: "extractive metallurgy",
    54020: "geology assistance",
    55022: "graphics",
    55023: "technical drawing",
    56025: "chemical plant operation",
    56026: "chemical laboratory",
    56027: "industrial chemistry (with mention)",
    57028: "knitting",
    57029: "textiles",
    57030: "clothing and textile manufacture",
    57031: "leather goods",
    58033: "connectivity and networks",
    58034: "programming",
    58035: "telecommunications",
    61001: "industrial food processing",
    61002: "collective catering",
    61003: "gastronomy (with mention)",
    62004: "early childhood care (62004)",
    62005: "elderly care",
    62006: "nursing care",
    62007: "social and recreational care",
    62008: "nursing care (with mention, 62008)",
    63009: "tourism services",
    63010: "hotel services",
    63011: "hospitality services",
    64001: "early childhood care",
    64008: "nursing care (with mention)",
    71001: "forestry",
    71002: "wood processing",
    71003: "wood products",
    71004: "pulp and paper",
    71005: "furniture and wood finishing",
    72006: "agriculture and livestock",
    72007: "agriculture and livestock (with mention)",
    81001: "merchant and special vessels",
    81002: "fishing",
    81003: "aquaculture",
    81004: "port operation",
    81005: "merchant and special vessel crew",
    91001: "visual arts",
    91002: "audiovisual arts",
    91003: "design",
    91004: "musical arts",
    91005: "performing arts",
    92004: "theatre performance",
    92005: "stage design",
    93006: "dance performance, intermediate level",
    93007: "dance instruction",
}
# Anexo X: the mentions of the specialties "with mention" (COD_MEN), in TP 3rd and 4th secondary from 2019; 0 is none.
TP_MENTIONS = {
    0: "no mention",
    41005001: "administration: common plan",
    41005002: "administration: logistics",
    41005003: "administration: human resources",
    51007001: "construction: common plan",
    51007002: "construction: building",
    51007003: "construction: construction finishing",
    51007004: "construction: roads and infrastructure",
    52013001: "industrial mechanics: common plan",
    52013002: "industrial mechanics: electromechanical maintenance",
    52013003: "industrial mechanics: machine tools",
    52013004: "industrial mechanics: die making",
    56027001: "industrial chemistry: common plan",
    56027002: "industrial chemistry: chemical plant",
    56027003: "industrial chemistry: chemical laboratory",
    61003001: "gastronomy: common plan",
    61003002: "gastronomy: cooking",
    61003003: "gastronomy: pastry and confectionery",
    64008001: "nursing care: elderly care",
    64008002: "nursing care: nursing",
    64008003: "nursing care: common plan",
    72007001: "agriculture and livestock: common plan",
    72007002: "agriculture and livestock: agriculture",
    72007003: "agriculture and livestock: livestock",
    72007004: "agriculture and livestock: wine growing",
}
CODE_LABELS = {
    "school_region": REGIONS,
    "residence_region": REGIONS,
    "school_dependency": {
        1: "municipal corporation",
        2: "municipal (DAEM)",
        3: "subsidised private",
        4: "private fee-paying",
        5: "delegated administration (DL 3166)",
        6: "local education service (SLEP)",
    },
    "school_rural": {0: "No", 1: "Yes"},
    "programme": {
        110: "basic",
        310: "secondary scientific-humanistic",
        410: "secondary TP commercial",
        510: "secondary TP industrial",
        610: "secondary TP technical",
        710: "secondary TP agricultural",
        810: "secondary TP maritime",
        910: "secondary artistic",
    },
    "shift": {1: "morning", 2: "afternoon", 3: "morning and afternoon", 4: "evening or night"},
    # The codebook names no type per combined-course code (0 simple course, 1 to 6 combined), so the six stay apart.
    "combined_course": {0: "No", **{k: f"combined {k}" for k in range(1, 7)}},
    "tp_course_type": {0: "not applicable", 1: "school only", 2: "dual (school and company)", 3: "other"},
    "tp_sector": TP_SECTORS,
    "tp_specialty": TP_SPECIALTIES,
    "tp_mention": TP_MENTIONS,
    "sex": {1: "male", 2: "female"},
    "final_status": STATUS,
    "prev_final_status": STATUS,
    "prev_programme": {
        2: "basic, children",
        3: "basic, adults",
        5: "secondary scientific-humanistic, youth",
        6: "secondary scientific-humanistic, adults",
        7: "secondary TP or artistic, youth",
        8: "secondary TP or artistic, adults",
    },
}
BASIC_GRADES = [f"{n} basic" for n in ("1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th")]
SECONDARY_GRADES = [f"{n} secondary" for n in ("1st", "2nd", "3rd", "4th")]
RENAME = {
    "rbd": "school_id",
    "cod_reg_rbd": "school_region",
    "cod_com_rbd": "school_commune",
    "cod_depe": "school_dependency",
    "rural_rbd": "school_rural",
    "cod_ense": "programme",
    "cod_jor": "shift",
    "cod_tip_cur": "combined_course",
    "cod_des_cur": "tp_course_type",
    "cod_sec": "tp_sector",
    "cod_espe": "tp_specialty",
    "cod_men": "tp_mention",
    "gen_alu": "sex",
    "fec_nac_alu": "birth_month",
    "edad_alu": "age_june_30",
    "cod_reg_alu": "residence_region",
    "cod_com_alu": "residence_commune",
    "prom_gral": "gpa",
    "asistencia": "attendance_pct",
    "sit_fin_r": "final_status",
    "prev_sit_fin_r": "prev_final_status",
    "prev_cod_ense2": "prev_programme",
    "prev_prom_gral": "prev_gpa",
    "prev_asistencia": "prev_attendance_pct",
}
CATEGORICAL = [
    "school_id",
    "school_region",
    "school_commune",
    "school_dependency",
    "school_rural",
    "programme",
    "shift",
    "combined_course",
    "tp_course_type",
    "tp_sector",
    "tp_specialty",
    "tp_mention",
    "sex",
    "residence_region",
    "residence_commune",
    "final_status",
    "prev_programme",
    "prev_final_status",
    "changed_school",
]


def _read_year(path: Path):
    """One yearly file: headers lower-cased without the byte-order mark, blanks missing, codes as integers."""
    import polars as pl

    frame = pl.read_csv(path, separator=";", infer_schema_length=0)
    frame = frame.rename({c: c.lstrip("﻿").strip().lower() for c in frame.columns})
    frame = frame.with_columns(
        pl.lit(None, dtype=pl.Utf8).alias(c) for c in OPTIONAL_INT_COLUMNS if c not in frame.columns
    )
    frame = frame.select(COLUMNS).with_columns(pl.col(c).str.strip_chars() for c in COLUMNS)
    frame = frame.with_columns(pl.when(pl.col(c) == "").then(None).otherwise(pl.col(c)).alias(c) for c in COLUMNS)
    return frame.with_columns(
        [pl.col(c).cast(pl.Int64) for c in INT_COLUMNS + OPTIONAL_INT_COLUMNS]
        + [pl.col(c).str.replace(",", ".").cast(pl.Float64) for c in DECIMAL_COLUMNS]
    )


def _final_rows(frame):
    """One row per student and year: the course the student ended the school year in.

    A student who changed school or course during the year has one row per course, all but the last coded
    SIT_FIN_R = "T" (transferred); their count is kept as `transfers_in_year`. Of the rows left (one per student for all
    but about 100 students a year) the first by status (promoted, failed, withdrawn, none), teaching code, school,
    grade and course letter is taken.
    """
    import polars as pl

    transfers = frame.group_by("mrun", maintain_order=True).agg(
        (pl.col("sit_fin_r") == "T").sum().cast(pl.Int16).alias("transfers_in_year")
    )
    final = frame.filter(pl.col("sit_fin_r").is_null() | (pl.col("sit_fin_r") != "T"))
    order = pl.col("sit_fin_r").replace_strict(STATUS_ORDER, default=3, return_dtype=pl.Int8)
    final = final.with_columns(order.alias("_order"))
    keys = ["mrun", "_order", "cod_ense", "rbd", "cod_grado", "let_cur"]
    final = final.sort(keys, maintain_order=True, nulls_last=True).unique("mrun", keep="first", maintain_order=True)
    return final.drop("_order", "let_cur").join(transfers, on="mrun", how="left")


def _next_state(frame):
    """Each student's state in a year's file: any regular course (children's or youth programme), else special
    education only, else adult education only.
    """
    import polars as pl

    regular = ~pl.col("cod_ense2").is_in(ADULT) & (pl.col("cod_ense2") != SPECIAL)
    state = (
        pl.when(regular.any())
        .then(pl.lit("regular"))
        .when((pl.col("cod_ense2") == SPECIAL).any())
        .then(pl.lit("special education"))
        .otherwise(pl.lit("adult education"))
    )
    return frame.group_by("mrun", maintain_order=True).agg(state.alias("next_state"))


def _grade_level():
    """The grade as one level from 1 (1st basic) to 12 (4th secondary), for the rows of children and youth."""
    import polars as pl

    return pl.when(pl.col("cod_ense2") == 2).then(pl.col("cod_grado")).otherwise(pl.col("cod_grado") + 8)


def _link_keys_known():
    """The rows a link may use: a birth month that is no placeholder, a sex and a home commune (0 is no information)."""
    import polars as pl

    return (pl.col("fec_nac_alu") != PLACEHOLDER_BIRTH_MONTH) & (pl.col("gen_alu") > 0) & (pl.col("cod_com_alu") > 0)


def _link_candidates(frame):
    """The rows of children and youth of one year's file that a new id may be linked by: id, keys and grade level."""
    import polars as pl

    rows = frame.filter(pl.col("cod_ense2").is_in(CHILD_YOUTH) & _link_keys_known())
    return rows.select("mrun", *LINK_KEYS, _grade_level().alias("level")).unique()


def _relink(absent, new):
    """The id changes: each absent student of year t with exactly one candidate among the ids new in t + 1 (same school,
    birth month, sex and home commune, at the same grade level or the next one), kept only where that new id is the
    candidate of this one absent student (one to one). Returns the pairs (`mrun`, `new_mrun`).
    """
    import polars as pl

    pairs = absent.join(new.rename({"mrun": "new_mrun", "level": "new_level"}), on=list(LINK_KEYS), how="inner")
    pairs = pairs.filter((pl.col("new_level") - pl.col("level")).is_in([0, 1])).select("mrun", "new_mrun").unique()
    pairs = pairs.filter(pl.col("mrun").count().over("mrun") == 1)
    return pairs.filter(pl.col("new_mrun").count().over("new_mrun") == 1)


def _population(final, state_next):
    """The rows of one year: students whose final course is in a children's or youth programme, without the graduates,
    with their state in the next year's file ("absent" when they are not in it).
    """
    import polars as pl

    rows = final.filter(pl.col("cod_ense2").is_in(CHILD_YOUTH))
    # Graduates leave the population: promoted from the 4th year of secondary in a youth programme.
    graduated = pl.col("cod_ense2").is_in(SECONDARY_YOUTH) & (pl.col("cod_grado") == 4) & (pl.col("sit_fin_r") == "P")
    rows = rows.filter(~graduated)
    return rows.join(state_next, on="mrun", how="left").with_columns(pl.col("next_state").fill_null("absent"))


def _decode_codes(df: pd.DataFrame, labels: dict) -> pd.DataFrame:
    """`decode` on each column's distinct codes (which checks every code has a label), mapped through a category."""
    for col, mapping in labels.items():
        codes = df[col].astype("category")
        words = decode(pd.DataFrame({col: codes.cat.categories}), {col: mapping})[col]
        df[col] = codes.map(dict(zip(codes.cat.categories, words, strict=True)))
    return df


class ChileSchoolDropoutMineduc1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will a Chilean school student who has not finished secondary school be out of regular schooling next "
            "school year?"
        ),
        use_case=(
            "When a school year closes, the Ministry of Education or a school's director ranks the students by their "
            "risk of not coming back to regular school next year, to target retention and re-enrolment before the new "
            "year starts (Rodriguez et al. 2023). The ministry's warning list covers 7th basic to 4th secondary; the "
            "rows cover every grade, as the source and the ministry's dropout rate do."
        ),
        row=(
            "One student of a children's or youth programme (1st basic to 4th secondary) in one school year from 2018 "
            "to 2024, in the course the student ended the year in; students promoted out of 4th secondary, the "
            "graduates, are left out (2.7 to 2.8 million students a year, Mineduc open data)."
        ),
        predicted=(
            "Whether the student has no course outside adult education in the next school year's records: absent "
            "from them, or in adult education only. A student whose id changed between the two years' records is "
            "linked to the new id by school, birth month, sex, home commune and grade, and counts as enrolled; deaths, "
            "emigration, graduation by examination and the id changes the link misses still count as dropouts."
        ),
        known=(
            "The year's school, its region, commune and type, the programme, grade, shift, course type and technical "
            "specialty; the "
            "student's sex, birth month, age and home commune; the year's grade average, attendance and final status "
            "(promoted, failed, withdrawn), and transfers during the year; the previous year's programme, status, "
            "grade average and attendance, and whether the school changed."
        ),
        split=(
            "The school years 2022, 2023 and 2024 are held out in turn (500,000 students each), each with a random "
            "million students of the earlier years from 2018 for training, as for a model refit every year."
        ),
        changes=(
            "We built the label by linking each student to the next year's records, re-linked the students whose id "
            "changed, added the previous year's record, left out the graduates and sampled the rows to the row budget."
        ),
        fit="approximate",
        fit_reason=(
            "Rows, inputs and yearly refit mirror an end-of-year warning list, though the ministry's covers grades "
            "7 to 12 only. The label is noisier than the source's: our re-link of changed ids is wrong for a "
            "tenth to a quarter of its links, and deaths, emigration and graduation by examination stay in (2.27% "
            "dropouts for 2019, 1.7% in the source). The source's family and welfare inputs are not in the files."
        ),
    )

    # Dataset
    unique_name = "chile_school_dropout_mineduc_1m"
    version_of = "chile_school_dropout_mineduc"
    version_comment = """
        We sample per test window (v2 split protocol): each yearly test window keeps at most 500k of its 2.8M students, and each train side is a random 1M of the students of all earlier years, drawn in one random order for all windows; the frame keeps only the rows a split uses.
    """
    year = "2026"
    domain = "education"
    source = "GOV Website"
    source_url = "https://datosabiertos.mineduc.cl/rendimiento-por-estudiante-2/"
    license = "CC BY-NC 2.0"  # the collection's entry on datos.gob.cl; the Mineduc portal states none
    data_tags = ("Spatial",)
    download_description = """
        We download the yearly files "Rendimiento por estudiante" of the school years 2017 to 2025 from the open data portal of the Centro de Estudios, Ministerio de Educacion de Chile (one RAR archive per year, each with one semicolon-separated CSV, the record layout and a frequency workbook), and unpack each archive into a folder named after it. Any RAR tool works (unrar, 7-Zip, or the Python package unrar-cffi, which we used).

        mkdir -p local-data-warehouse/chile_school_dropout_mineduc && cd local-data-warehouse/chile_school_dropout_mineduc
        for u in 2021/12/Rendimiento-2017 2021/12/Rendimiento-2018 2021/12/Rendimiento-2019 2021/12/Rendimiento-2020 2022/04/Rendimiento-2021 2023/02/Rendimiento-2022 2024/09/Rendimiento-2023 2025/04/Rendimiento_2024 2026/03/Rendimiento-por-estudiante-2025; do wget "https://datosabiertos.mineduc.cl/wp-content/uploads/$u.rar"; done
        for f in *.rar; do mkdir -p "${f%.rar}" && unrar x "$f" "${f%.rar}/"; done
    """
    bibtex = """
        @misc{mineduc2026rendimiento,
          author = {{Centro de Estudios, Ministerio de Educaci{\\'o}n de Chile}},
          title = {Rendimiento por estudiante: bases de datos de rendimiento escolar por estudiante con MRUN, 2002--2025},
          year = {2026},
          howpublished = {\\url{https://datosabiertos.mineduc.cl/rendimiento-por-estudiante-2/}},
          note = {Datos Abiertos Mineduc; yearly files, the 2025 file published in March 2026},
        }
    """
    curation_comments = """
        We start with the yearly files "Rendimiento por estudiante" (every student's final status in a school year) of 2017 to 2025 from the open data portal of Mineduc's Centro de Estudios, and build the task of Rodriguez, Villanueva, Dombrovskaia and Valenzuela, "A methodology to design, develop, and evaluate machine learning models for predicting dropout in school systems: the case of Chile", Education and Information Technologies 28, 2023 (doi:10.1007/s10639-022-11515-5).

        - Prediction point: the close of school year t, once the final statuses are recorded (each file is cut at the end of January of t + 1) and before the next year starts in March. Everything of year t and earlier is known then; the label comes from the file of t + 1. The source predicts from the same point: its final model uses whether the last grade was approved and the last cycle's attendance (Appendix B, Table 11).
        - Rows: one per student (pseudonymised id MRUN) and school year t from 2018 to 2024 whose final course is in a children's or youth programme (grouped teaching level 2, 5 or 7). Students promoted out of 4th secondary have graduated and leave, as in the source; adult education (3, 6, 8) is the outcome and special education (4, in the files from 2023) is no row. A student who moved from a youth to an adult course during year t ends the year in adult education and is no row either (8,526 in 2023, 91% of them dropouts by the label); the source counts every student enrolled in a children's or youth grade in t, but the final course is known at the prediction point, so the left-out students are chosen by an input, not by the outcome.
        - The final course: a student who changed course during the year has one row per course, all but the last coded SIT_FIN_R = "T" (transferred); we keep the row that is no transfer and count the others in `transfers_in_year`. For the 16 to 240 students a year with two such rows, the first by status (promoted, failed, withdrawn, none), teaching code, school, grade and course letter.
        - The target `dropout` ("Yes"): no course outside adult education in the file of t + 1 (absent, or adult education only), the source's definition (Sec. 3.2) and Mineduc's dropout rate of the regular system (2.4% for 2018). After the re-link below: 2.2% to 2.3% of the rows before 2020, 1.2% and 1.7% in the COVID-19 years 2020 and 2021, 2.3% to 2.5% from 2022 on; 59% to 79% of them absent, the rest in adult education.
        - Re-link of changed ids (`_relink`): Mineduc gives a foreign student without a national id (RUN) a provisional school id (IPE) and moves the record to the RUN once it is issued, so the student's MRUN changes between two yearly files and the student reads as absent. An absent student of year t with a known birth month, sex and home commune is linked when exactly one id new in t + 1 (in no file from 2017 to t) has a children's or youth row in t + 1 at the same school, with the same sex, birth month and home commune, at the same grade or the next one, one to one. The linked student counts as enrolled (state `relinked`, label "No"; relabelled, never dropped, which would choose the rows by the file of t + 1), and the new id's row of t + 1 takes the old id's previous year. Links for 2018 to 2024: 6,934, 7,819, 7,458, 5,753, 10,526, 12,935 and 14,880, 10% to 19% of each year's dropouts, more in the test windows; the dropout rate falls from 2.46% and 2.56% to 2.21% and 2.27% in 2018 and 2019, and from 2.77%, 2.92% and 2.80% to 2.40%, 2.46% and 2.27% in 2022 to 2024. Wrong links, by a placebo with the birth month shifted by one or two months: 10% to 26% of the links (15% to 32% when a shifted month may take a real partner; 5% to 18% by enrolled controls), 2021 the worst, so the link removes three to nine wrong dropouts for each one it adds. Linked students come back under their old id two years on at 2% to 6%, against 14% to 26% of the unlinked promoted absent students.
        - Anomaly: deaths, emigration, graduation by examination and the id changes the link misses (a change of school as well, or several candidates) still count as dropouts. The source removed deaths and graduates by other routes with the ministry's own lists (Table 1), which we found neither on the Mineduc portal nor on datos.gob.cl, and reports 1.7% for 2019 against our 2.27%. Mineduc's graduates files separate the routes only from 2025 (every graduate of 2017 to 2024 is ORIGEN = RENDIMIENTO): about 970 of the 78,300 dropouts of 2024 before the re-link (1.2%) graduate in 2025 by examination or another route; not relabelled, as only the newest window could be.
        - Anomaly: special education enters the files in 2023, so a move into it counts as enrolled for the labels of 2022 on (3,025, 1,619 and 1,502 students) and as a dropout before, where it cannot be seen. A previous year in special education (1.2% of the 2024 rows) reads as "not enrolled" with the previous-year columns missing, as the same students read in every earlier year (one definition per column over time).
        - The previous year: the student's final course in the file of t - 1, any programme (for a re-linked student, the old id's): `prev_programme` ("not enrolled" when absent), `prev_final_status`, `prev_gpa`, `prev_attendance_pct` and `changed_school`, one year of the source's trajectory descriptors (24 of its 111 variables, Table 3).
        - Dropped: MRUN (the join key; it also encodes the id change: MRUN alone scores ROC AUC 0.678 on the raw rows, 0.715 before the re-link) and the course letter; SIT_FIN (an exact copy of SIT_FIN_R on the rows kept); the names of school, commune, department and region (copies of codes) and the RBD check digit; the province, provincial department, COD_DEPE2, COD_ENSE2 (used for the rows) and COD_RAMA (groupings of kept codes); ESTADO_ESTAB (near-constant, not "operating" in at most 25 rows a year, and possibly written at extraction, after the prediction point); NOMBRE_SLEP (only from 2024, set exactly on the rows of dependency 6).
        - Proxy missing values (CLEAN-10): sex 0 and residence 0 ("Sin información"), birth month 190001. An age of 4 or under in a school grade (123 rows in 1st to 7th basic) is impossible (CLEAN-11): age and birth month missing; ages of 30 and over in children's programmes (138 rows) stay as published, unusual. A grade average of 0.0 is no grade on the 1.0 to 7.0 scale (withdrawn students; special and adult education, graded otherwise: 28,897 of 30,459 special-education courses of 2023), so `gpa` is missing when the year ended withdrawn or without a status, or at 0.0, and `attendance_pct` in the same years or at 0 with a 0.0 average; the same for the previous year.
        - Dtypes: the codebook's codes are decoded into English words (CLEAN-12), `grade` ordered from 1st basic to 4th secondary; the TP sector and specialty from Anexo VI (0 is "general cycle or not applicable"), the TP mention from Anexo X (in TP 3rd and 4th secondary only, "no mention" for a specialty without one; missing in 2018, whose file has no mention). `combined_course` keeps the six combined-course codes ("combined 1" to "combined 6"), which the codebook does not name. The school id (RBD) and the communes keep their official codes as categories, as CLEAN-12 has it for an entity's name and for a code nested in its region. `age_june_30` (the codebook's age) equals the age computed from `birth_month` wherever both exist; kept as published.
        - Note: year t's final status, grade average, attendance and transfers are inputs at this prediction point. Withdrawn students are 1.3% of the rows and 41% of the dropouts after the re-link (the decision "Dropout by the year's final status"); untuned LightGBM (3 windows, 300k training rows) reaches ROC AUC 0.87 to 0.88 with them, 0.74 to 0.76 without, and 0.77 to 0.79 on the students not withdrawn.
        - Note: `school_id` stays: schools recur every year (99.9% of the test rows have their school in training), a known entity (CLEAN-3, USE-10). It costs untuned LightGBM 0.008 to 0.013 ROC AUC in the same runs, the model's handling of an 8,712-level category (CLEAN-22).
        - Duplicates: 813 rows (0.03%) repeat another row, 12 with the other label; no test row has a copy on its training side. Distinct students with the same record; kept.
        - Note: sex stays an input; the use case offers support, not a decision against the student. The Ñuble region (16) and its communes take new codes from 2018.
        - Licence: CC BY-NC 2.0 is the collection's entry on datos.gob.cl; the Mineduc portal states none. Non-commercial; to confirm for the release.
        - The year is that of the snapshot we pin (PROV-9): the newest file, of 2025, was published in March 2026. The files of 2002 to 2016 are not downloaded (SPLIT-20: a recent history); 2017 serves only as the previous year of 2018 and as earlier ids for the re-link.
    """

    # Task
    target = "dropout"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Rodriguez et al. (2023) measure performance by one criterion, the geometric mean (GM) of sensitivity and "
            "specificity (Sec. 2.2), the objective of their feature selection (Sec. 2.4) and the measure that picks "
            "their model (Sec. 3.2); F1 and the recall and precision of both classes are reported beside it. GM is a "
            "threshold metric, taken at the default cut of a training set undersampled to 1:1, and neither the paper "
            "nor the decision fixes a threshold or a cost (MET-6), so the fallback. Mineduc's early warning system "
            "publishes no metric."
        )
    )

    # Splits
    splits_comment = """
        We hold out each of the last 3 school years in turn (2024, 2023, 2022, newest first; the labels come from the files of 2025, 2024 and 2023) and train on every earlier school year from 2018, as for a model refit once a year. No gap: the label of year t - 1 is the enrolment in year t, which is known when year t closes. The history starts in 2018 (the 2017 file gives its previous year) and holds the COVID-19 years 2020 and 2021, when fewer students left (1.2% and 1.7% against 2.2% to 2.3% before and 2.3% to 2.5% after) and attendance was recorded differently: 100% for 45.3% and 24.1% of the rows (4% to 6% in the other years), and a dropout rate of 7.6% and 4.9% under 50% attendance against 15% to 26% in the other years. They stay: a yearly refit would have trained on them, and without them the 2022 window would train on 2 of 7 years, under half the rows (SPLIT-14). The label changes inside the history too (SPLIT-20): special education enters the files in 2023, so a move into it is "No" in the labels from 2022 on and "Yes" before (2% to 5% of a year's dropouts); the windows of 2023 and 2024 train on both. Each test window keeps at most 500k of its 2.8M students, and each train side is a random 1M of the students of the earlier years (one random order for all windows).

        Protocol (LEAK-9): a model sees only its split's rows. The rows of a later window hold many of the same students one year on, whose `prev_gpa` and `prev_attendance_pct` repeat year t's values and whose presence tells the label; a participant who matched them gained 0.017 ROC AUC on the 2023 and 2022 windows (none on 2024, with no later rows).
    """
    temporal = Temporal(
        on="year",
        splits=TemporalSplits(window=1, unit="unique", n_windows=3),
        horizon=1,
        horizon_unit="years",
    )
    row_budget = RowBudget(train=1_000_000, test=500_000)

    prepared_raw_files = (PREPARED,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # One row per student of a children's or youth programme in year t, with the state in the next year's file
        # and the final row of the previous year, joined on the pseudonymised student id (MRUN), the source's key.
        # A student whose id changed between the two files (a provisional school id replaced by the national id) is
        # re-linked: the state "relinked" (label "No"), and the new id's row of t + 1 takes the old id's history.
        import polars as pl

        files = {y: sorted((raw_dir / folder).glob("*.csv")) for y, folder in YEAR_FOLDERS.items()}
        assert all(len(f) == 1 for f in files.values()), f"expected one CSV per year folder: {files}"
        final, state, ids, candidates = {}, {}, {}, {}
        for y, (path,) in files.items():
            frame = _read_year(path)
            final[y] = _final_rows(frame)
            state[y] = _next_state(frame)
            ids[y] = frame.select("mrun").unique()
            candidates[y] = _link_candidates(frame)
            del frame
        first = min(files)
        population, links = {}, {}
        for t in (first, *YEARS):
            rows = _population(final[t], state[t + 1])
            # The ids of t + 1 found in no file from the first year to t, and the absent students who may link to them.
            seen = pl.concat([ids[y] for y in range(first, t + 1)]).unique()
            new = candidates[t + 1].join(seen, on="mrun", how="anti")
            absent = rows.filter((pl.col("next_state") == "absent") & _link_keys_known())
            links[t] = _relink(absent.select("mrun", *LINK_KEYS, _grade_level().alias("level")), new)
            relinked = pl.col("mrun").is_in(links[t]["mrun"].implode())
            population[t] = rows.with_columns(
                pl.when(relinked).then(pl.lit("relinked")).otherwise(pl.col("next_state")).alias("next_state")
            )
        frames = []
        for t in YEARS:
            rows = population[t]
            # The history: the final row of t - 1, read under the old id for a new id re-linked from year t - 1.
            old_ids = links[t - 1].select(pl.col("new_mrun").alias("mrun"), pl.col("mrun").alias("history_mrun"))
            rows = rows.join(old_ids, on="mrun", how="left")
            rows = rows.with_columns(pl.col("history_mrun").fill_null(pl.col("mrun")))
            prev = final[t - 1].select(
                pl.col("mrun").alias("history_mrun"),
                pl.col("rbd").alias("prev_rbd"),
                pl.col("cod_ense2").alias("prev_cod_ense2"),
                pl.col("sit_fin_r").alias("prev_sit_fin_r"),
                pl.col("prom_gral").alias("prev_prom_gral"),
                pl.col("asistencia").alias("prev_asistencia"),
            )
            rows = rows.join(prev, on="history_mrun", how="left").drop("history_mrun")
            frames.append(rows.with_columns(pl.lit(t, dtype=pl.Int16).alias("year")).sort("mrun"))
        pl.concat(frames).write_parquet(raw_dir / PREPARED)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_parquet(raw_dir / PREPARED)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # 1. The target: no course outside adult education in the next school year's file (absent, or in adult
        #    education only), the definition of Rodriguez et al. (2023, Sec. 3.2). A student re-linked to a new id
        #    (`_relink`) is enrolled: "No".
        df[self.target] = np.where(df["next_state"].isin(["absent", "adult education"]), "Yes", "No")
        # 2. Special education enters the files in 2023: a previous year in it reads as "not enrolled", as the same
        #    students read in every earlier year (one definition per column over time).
        prev_special = df["prev_cod_ense2"] == SPECIAL
        for col in ("prev_rbd", "prev_cod_ense2", "prev_sit_fin_r", "prev_prom_gral", "prev_asistencia"):
            df[col] = df[col].mask(prev_special)
        # 3. A change of school since the previous year's final course (missing without a previous year).
        df["changed_school"] = np.where(df["prev_rbd"].isna(), None, np.where(df["prev_rbd"] == df["rbd"], "No", "Yes"))
        # 4. The TP mention exists only in TP and artistic 3rd and 4th secondary (and in the files from 2019).
        tp_upper = (df["cod_ense2"] == 7) & df["cod_grado"].isin([3, 4])
        df["cod_men"] = df["cod_men"].where(tp_upper)
        # 5. Identifiers and bookkeeping: the student id (the join key), the next year's state (the label), the
        #    previous school (used by step 3) and the grouped teaching level (the population filter).
        df = drop_columns(df, ["mrun", "next_state", "prev_rbd", "cod_ense2"])
        df = df.rename(columns=RENAME)
        # 6. Proxy missing values (CLEAN-10): sex 0 and residence 0 mean no information (codebook); a birth month of
        #    1900-01 is a placeholder. An age of 4 or under in a school grade is impossible (CLEAN-11; the codebook
        #    calls atypical ages entry errors): age and birth month go missing. A grade average of 0.0 is no grade
        #    (the scale is 1.0 to 7.0): the codebook reports it for a withdrawn student and for courses graded on
        #    other scales (special and adult education); the attendance goes missing with it, and for any year that
        #    ended withdrawn or without a status.
        for col, code in (("sex", 0), ("residence_region", 0), ("residence_commune", 0)):
            df[col] = df[col].mask(df[col] == code)
        too_young = df["age_june_30"] <= 4
        df["age_june_30"] = df["age_june_30"].mask(too_young)
        df["birth_month"] = df["birth_month"].mask((df["birth_month"] == PLACEHOLDER_BIRTH_MONTH) | too_young)
        for prefix in ("", "prev_"):
            no_grade = ~df[f"{prefix}final_status"].isin(["P", "R"])
            no_record = no_grade | ((df[f"{prefix}gpa"] == 0) & (df[f"{prefix}attendance_pct"] == 0))
            df[f"{prefix}attendance_pct"] = df[f"{prefix}attendance_pct"].mask(no_record)
            df[f"{prefix}gpa"] = df[f"{prefix}gpa"].mask(no_grade | (df[f"{prefix}gpa"] == 0))
        # 7. Codes to the codebook's words (CLEAN-12), the TP sector, specialty and mention from Anexos VI and X; the
        #    schools and communes keep their official codes (an entity's name, and a code nesting in the region). The
        #    grade is an ordered scale over basic and secondary (CLEAN-14).
        df["grade"] = np.where(
            df["programme"] == 110,
            df["cod_grado"].map(dict(enumerate(BASIC_GRADES, start=1))),
            df["cod_grado"].map(dict(enumerate(SECONDARY_GRADES, start=1))),
        )
        df = drop_columns(df, ["cod_grado"])
        df = _decode_codes(df, CODE_LABELS)
        df["prev_programme"] = df["prev_programme"].astype(object).where(df["prev_programme"].notna(), "not enrolled")
        for col in ("school_id", "school_commune", "residence_commune"):
            df[col] = df[col].astype("Int64").astype("string").astype(object)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=CATEGORICAL,
            datetime={"birth_month": "%Y%m"},
            ordinal={"grade": BASIC_GRADES + SECONDARY_GRADES},
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        # The label's parts by school year: where the students of year t are in the file of t + 1.
        state = pd.crosstab(raw["year"], raw["next_state"])
        state["dropout share"] = (state["absent"] + state["adult education"]) / state.sum(axis=1)
        state["dropout share"] = state["dropout share"].map("{:.2%}".format)
        # The prediction point: how much of the label year t's final status already carries.
        status = raw["sit_fin_r"].map(STATUS).fillna("none").rename("final status of year t")
        dropout = raw["next_state"].isin(["absent", "adult education"])
        by_status = pd.DataFrame({"students": status.value_counts(), "dropouts": dropout.groupby(status).sum()})
        by_status["dropout rate"] = (by_status["dropouts"] / by_status["students"]).map("{:.1%}".format)
        by_status["share of all dropouts"] = (by_status["dropouts"] / dropout.sum()).map("{:.1%}".format)
        return [
            Decision(
                "Next year's state",
                "The label: a student of year t is a dropout when the file of t + 1 holds no course of theirs outside "
                "adult education (absent, or adult education only). An absent student re-linked to a new id in the "
                "file of t + 1 (`relinked`) is enrolled. Special education is in the files from 2023 on.",
                state,
            ),
            Decision(
                "Dropout by the year's final status",
                "The prediction point is the close of year t, so the year's final status is an input; a student "
                "withdrawn during the year is most often a dropout, and those students hold a large share of them.",
                by_status.sort_values("students", ascending=False, kind="stable"),
            ),
        ]
