"""Curated dataset definition for `enem_entrance_exam_scores_1m` (data-foundry v2). Evidence: README.md."""

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

EDITIONS = tuple(range(2018, 2024))
"""The editions we read: 2018 to 2023. From 2024 on, INEP publishes the registrants and the scores in two files with no
common key (Leia-me 2024, section 3), so 2023 is the newest edition with both in one row."""

ZIP = "raw/microdados_enem_{edition}.zip"
MEMBER = "DADOS/MICRODADOS_ENEM_{edition}.csv"
"""The CSV in each zip; the 2023 zip nests it in a folder microdados_enem_2023/."""

SAMPLE_FRACTION = 0.25
"""The share of each edition's participants `_prepare_raw_files` keeps (uniformly), so the frame fits in memory: 2021,
the smallest edition, keeps 559,527 participants, above the 500k a test window uses."""

SAMPLE_SEED = 42
"""The draw of edition t uses the seed SAMPLE_SEED + t."""

PREPARED = "participants_2018_2023_sample.parquet"
PREPARED_COUNTS = "participants_2018_2023_counts.csv"

PRESENCE = ("TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT")
"""Presence at the four objective tests: 0 absent, 1 present, 2 eliminated (day 1: CH and LC, day 2: CN and MT)."""

SCORES = ("NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO")
"""The five scores: natural sciences, humanities, languages, mathematics (IRT scales) and the essay (0 to 1000)."""

REGISTRATION = {
    "NU_ANO": "edition",
    # the registrant (dictionary, "Dados do participante")
    "TP_FAIXA_ETARIA": "age_band",
    "TP_SEXO": "sex",
    "TP_ESTADO_CIVIL": "marital_status",
    "TP_COR_RACA": "race",
    "TP_NACIONALIDADE": "nationality",
    "TP_ST_CONCLUSAO": "secondary_school_status",
    "TP_ANO_CONCLUIU": "years_since_secondary",
    "TP_ESCOLA": "secondary_school_type",
    "TP_ENSINO": "secondary_school_modality",
    "IN_TREINEIRO": "practice_only",
    # the secondary school, for those whose school INEP identified ("Dados da escola")
    "CO_MUNICIPIO_ESC": "school_municipality",
    "SG_UF_ESC": "school_state",
    "TP_DEPENDENCIA_ADM_ESC": "school_administration",
    "TP_LOCALIZACAO_ESC": "school_location",
    # the exam place, chosen at registration ("Dados do local de aplicação da prova")
    "CO_MUNICIPIO_PROVA": "exam_municipality",
    "SG_UF_PROVA": "exam_state",
    # the foreign-language test, chosen at registration
    "TP_LINGUA": "foreign_language",
    # the socioeconomic questionnaire, answered at registration
    "Q001": "father_education",
    "Q002": "mother_education",
    "Q003": "father_occupation",
    "Q004": "mother_occupation",
    "Q005": "household_size",
    "Q006": "family_income",
    "Q007": "domestic_worker",
    "Q008": "bathrooms",
    "Q009": "bedrooms",
    "Q010": "cars",
    "Q011": "motorcycles",
    "Q012": "refrigerators",
    "Q013": "freezers",
    "Q014": "washing_machines",
    "Q015": "clothes_dryers",
    "Q016": "microwaves",
    "Q017": "dishwashers",
    "Q018": "vacuum_cleaner",
    "Q019": "colour_tvs",
    "Q020": "dvd_player",
    "Q021": "pay_tv",
    "Q022": "mobile_phones",
    "Q023": "landline",
    "Q024": "computers",
    "Q025": "internet",
}
"""The columns known at registration, with our names. Not read: the registration number (a mask, dictionary note 1),
the state codes (copies of the state abbreviations), the school's operating status (TP_SIT_FUNC_ESC, from a school
census of undocumented year), the test versions, the answer and key strings, the essay status and its five competence
scores (all from the exam days), and 2018's Q026 and Q027 (asked that year only)."""

MUNICIPALITY_NAMES = {"school_municipality": "NO_MUNICIPIO_ESC", "exam_municipality": "NO_MUNICIPIO_PROVA"}
"""The names INEP gives each municipality code in the same file; `_clean` decodes the codes into "Name (UF) [code]"."""

# The dictionaries' words for the codes, in English (Dicionário_Microdados_Enem_<edition>.xlsx). The codes are the same
# in every edition from 2019 on; 2018 numbers the marital status from 0 and records the school type otherwise
# (MARITAL_2018, SCHOOL_TYPE_2018).
AGE_BANDS = {
    1: "under 17",
    2: "17",
    3: "18",
    4: "19",
    5: "20",
    6: "21",
    7: "22",
    8: "23",
    9: "24",
    10: "25",
    11: "26 to 30",
    12: "31 to 35",
    13: "36 to 40",
    14: "41 to 45",
    15: "46 to 50",
    16: "51 to 55",
    17: "56 to 60",
    18: "61 to 65",
    19: "66 to 70",
    20: "over 70",
}
"""Age on 31 December of the edition's year (dictionary note 2)."""

MARITAL = {1: "single", 2: "married or living with a partner", 3: "divorced or separated", 4: "widowed"}
MARITAL_2018 = {"0": "1", "1": "2", "2": "3", "3": "4"}
"""2018's codes 0 to 3 (single to widowed, no "not informed") onto the codes of 2019 on."""

SCHOOL_TYPE_2018 = {"2": "2", "3": "2", "4": "3"}
"""2018's TP_ESCOLA is the administration of the school INEP matched, not the registrant's answer of 2019 on: 2 state,
3 municipal (the dictionary's "abroad"), 4 private, and 1 ("Não respondeu") for federal schools and the unmatched. We
map state and municipal schools to public (2) and private schools to private (3), the code of 2019 on; a federal
school's 1 becomes public in `_clean`, every other 1 stays missing."""

SCHOOL_TYPE_FEDERAL = "1"
"""TP_DEPENDENCIA_ADM_ESC of a federal school."""

FINISHING_THIS_YEAR = "2"
"""TP_ST_CONCLUSAO of those finishing secondary school in the edition's year: the only status whose modality
(TP_ENSINO) every edition fills."""

EJA = "3"
"""TP_ENSINO's youth and adult education (EJA), recorded in 2018 only."""

YEARS_SINCE_CAP = 12
"""TP_ANO_CONCLUIU counts back from the edition (1 = the year before) to a last level "before 2007": code 12 in 2018,
17 in 2023. We cap every edition at 12 years, the 2018 edition's last level, so a level means the same everywhere."""

YEARS_SINCE_LEVELS = [str(k) for k in range(1, YEARS_SINCE_CAP)] + [f"{YEARS_SINCE_CAP} or more"]

PARENT_EDUCATION = {
    "A": "never studied",
    "B": "did not complete the 5th year of primary school",
    "C": "completed the 5th but not the 9th year of primary school",
    "D": "completed primary school (9th year), not secondary school",
    "E": "completed secondary school, not college",
    "F": "completed college, not a postgraduate degree",
    "G": "completed a postgraduate degree",
}
"""Q001 (the father or the man responsible) and Q002 (the mother or the woman responsible); H, "Não sei", is missing."""

OCCUPATION = {
    "A": "group 1: farm, fishing and extractive work without employees",
    "B": "group 2: domestic, cleaning, security, retail and office support work",
    "C": "group 3: skilled manual, factory, construction and driving work",
    "D": "group 4: teacher, technician, police, supervisor, small business owner, self-employed",
    "E": "group 5: physician, engineer, lawyer, officer, professor, director, owner of a business with over 10 staff",
}
"""Q003 and Q004, "grupos ordenados" in the dictionary's words; F, "Não sei", is missing."""

INCOME = {
    "A": "no income",
    "B": "up to 1 minimum wage",
    "C": "1 to 1.5 minimum wages",
    "D": "1.5 to 2 minimum wages",
    "E": "2 to 2.5 minimum wages",
    "F": "2.5 to 3 minimum wages",
    "G": "3 to 4 minimum wages",
    "H": "4 to 5 minimum wages",
    "I": "5 to 6 minimum wages",
    "J": "6 to 7 minimum wages",
    "K": "7 to 8 minimum wages",
    "L": "8 to 9 minimum wages",
    "M": "9 to 10 minimum wages",
    "N": "10 to 12 minimum wages",
    "O": "12 to 15 minimum wages",
    "P": "15 to 20 minimum wages",
    "Q": "over 20 minimum wages",
}
"""Q006, the family's monthly income. The dictionaries give the bands in reais; every edition's bounds are these
multiples of that year's minimum wage (R$ 954 in 2018, 998, 1,045, 1,100, 1,212, R$ 1,320 in 2023)."""

DOMESTIC_WORKER = {"A": "no", "B": "1 or 2 days a week", "C": "3 or 4 days a week", "D": "5 or more days a week"}
"""Q007, a paid domestic worker in the home."""

COUNT = {"A": "0", "B": "1", "C": "2", "D": "3", "E": "4 or more"}
"""How many of an item the home has ("Não", "Sim, um", "Sim, dois", "Sim, três", "Sim, quatro ou mais")."""

COUNT_QUESTIONS = (
    "bathrooms",
    "bedrooms",
    "cars",
    "motorcycles",
    "refrigerators",
    "freezers",
    "washing_machines",
    "clothes_dryers",
    "microwaves",
    "dishwashers",
    "colour_tvs",
    "mobile_phones",
    "computers",
)
YES_NO = {"A": "No", "B": "Yes"}
YES_NO_QUESTIONS = ("vacuum_cleaner", "dvd_player", "pay_tv", "landline", "internet")

CODE_LABELS = {
    "age_band": AGE_BANDS,
    "sex": {"M": "male", "F": "female"},
    "marital_status": MARITAL,
    "race": {1: "white", 2: "black", 3: "brown (parda)", 4: "asian (amarela)", 5: "indigenous"},
    "nationality": {1: "Brazilian", 2: "naturalised Brazilian", 3: "foreign", 4: "Brazilian born abroad"},
    "secondary_school_status": {
        1: "already completed",
        2: "completing in the edition's year",
        3: "completing after the edition's year",
        4: "not completed and not enrolled",
    },
    "secondary_school_type": {2: "public", 3: "private", 4: "abroad"},
    "secondary_school_modality": {1: "regular", 2: "special education"},
    "school_administration": {1: "federal", 2: "state", 3: "municipal", 4: "private"},
    "school_location": {1: "urban", 2: "rural"},
    "foreign_language": {0: "English", 1: "Spanish"},
    "father_education": PARENT_EDUCATION,
    "mother_education": PARENT_EDUCATION,
    "father_occupation": OCCUPATION,
    "mother_occupation": OCCUPATION,
    "family_income": INCOME,
    "domestic_worker": DOMESTIC_WORKER,
    **dict.fromkeys(COUNT_QUESTIONS, COUNT),
    **dict.fromkeys(YES_NO_QUESTIONS, YES_NO),
}

PROXY_MISSING = {
    "marital_status": ["0"],  # "Não informado" (2019 on)
    "race": ["0", "6"],  # "Não declarado"; "Não dispõe da informação" (6, from 2021 on)
    "nationality": ["0"],  # "Não informado"
    "secondary_school_type": ["1"],  # "Não respondeu"
    "father_education": ["H"],  # "Não sei"
    "mother_education": ["H"],
    "father_occupation": ["F"],  # "Não sei"
    "mother_occupation": ["F"],
}
"""Codes that mean unknown (CLEAN-10). TP_ANO_CONCLUIU 0, "Não informado", goes missing with the cap (step 3)."""

ORDINAL = {
    "age_band": list(AGE_BANDS.values()),
    "years_since_secondary": YEARS_SINCE_LEVELS,
    "father_education": list(PARENT_EDUCATION.values()),
    "mother_education": list(PARENT_EDUCATION.values()),
    "father_occupation": list(OCCUPATION.values()),
    "mother_occupation": list(OCCUPATION.values()),
    "family_income": list(INCOME.values()),
    "domestic_worker": list(DOMESTIC_WORKER.values()),
    **{key: list(COUNT.values()) for key in COUNT_QUESTIONS},
}

CATEGORICAL = [
    "sex",
    "marital_status",
    "race",
    "nationality",
    "secondary_school_status",
    "secondary_school_type",
    "secondary_school_modality",
    "school_municipality",
    "school_state",
    "school_administration",
    "school_location",
    "exam_municipality",
    "exam_state",
    "foreign_language",
    *YES_NO_QUESTIONS,
]


def _decode_codes(df: pd.DataFrame, labels: dict) -> pd.DataFrame:
    """`decode` on each column's distinct codes (which checks every code has a label), mapped through a category."""
    for col, mapping in labels.items():
        codes = df[col].astype("category")
        words = decode(pd.DataFrame({col: codes.cat.categories}), {col: mapping})[col]
        df[col] = codes.map(dict(zip(codes.cat.categories, words, strict=True)))
    return df


def _municipality_labels(df: pd.DataFrame, col: str, name_col: str, state_col: str) -> pd.Series:
    """The IBGE code in `col` as "Name (UF) [code]", with the name and state the file gives it. Within an edition each
    code has one name and state and each name and state one code (checked); 13 codes were renamed between editions
    (a spelling or a new name), and those take the newest edition's name.
    """
    pairs = df[["edition", col, name_col, state_col]].dropna(subset=[col]).drop_duplicates()
    per_edition = pairs.groupby(["edition", col])[[name_col, state_col]].nunique()
    codes_per_name = pairs.groupby(["edition", name_col, state_col])[col].nunique()
    if pairs[name_col].isna().any() or per_edition.to_numpy().max() > 1 or codes_per_name.max() > 1:
        raise ValueError(f"{col}: the codes and the names of {name_col} are not one to one within an edition")
    newest = pairs.sort_values("edition", kind="stable").groupby(col).last()
    labels = newest[name_col] + " (" + newest[state_col] + ") [" + newest.index + "]"
    return df[col].map(labels)


class EnemEntranceExamScores1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What mean score over the five tests will a registrant of Brazil's national secondary-school exam (ENEM) "
            "reach, judged from the registration form?"
        ),
        use_case=(
            "For example, an NGO or a public cursinho programme (MEC's CPOP), or a state department filling limited "
            "places, asks its applicants the ENEM registration items on its own intake form when registration closes, "
            "months before the exam, and ranks them by expected ENEM mean score, to give free preparation places to "
            "those likely to stay below the 450 points that ProUni scholarships and FIES loans require."
        ),
        row=(
            "One registrant of one ENEM edition, 2018 to 2023, who sat both exam days: a uniform quarter of each "
            "edition's 2.2 to 3.9 million such participants, from INEP's microdata."
        ),
        predicted=(
            "The mean of the registrant's five scores (natural sciences, humanities, languages, mathematics and the "
            "essay), on INEP's scales of up to about 1000 points, published about three months after the exam."
        ),
        known=(
            "The registration form: age band, sex, race, marital status, nationality, secondary-school status, type "
            "and year, the school's municipality and administration when known, the exam municipality, the foreign "
            "language, and the socioeconomic questionnaire (parents' schooling and work, family income, household "
            "goods)."
        ),
        split=(
            "The editions 2021, 2022 and 2023 are held out in turn (500,000 participants each), each with a random "
            "million participants of the earlier editions from 2018 for training, as for a model refit every year."
        ),
        changes=(
            "We keep the participants present on both days, build the mean of the five scores, drop everything "
            "recorded on or after the exam days, align 2018's codes with the later editions', put the codes into "
            "words, and sample the rows to the row budget."
        ),
        fit="approximate",
        fit_reason=(
            "INEP names no prediction and holds the form itself (Edital 30/2023, 14.8-14.9); a department would also "
            "hold grades and state assessments, absent here. Rows are those who sat both days, unknown at "
            "registration: a third stay away, more of the poorest (2023: 38% absent at up to 1 minimum wage, 18% "
            "above 4). Treineiros, 17-19% of rows, cannot use the edition for ProUni or FIES; repeat registrants "
            "cannot be linked."
        ),
    )

    # Dataset
    unique_name = "enem_entrance_exam_scores_1m"
    version_of = "enem_entrance_exam_scores"
    version_comment = """
        The task is every participant present on both days of the editions 2018 to 2023: 17,445,513 participants. `_prepare_raw_files` keeps a uniform quarter of each edition, 4,361,378 participants (559,527 in 2021 to 973,432 in 2018), so the frame fits in memory; the v2 split protocol then keeps at most 500k participants of each yearly test window and a random 1M of the participants of the earlier editions for each train side (one random order for all windows), and the frame keeps only the rows a split uses.
    """
    year = "2026"
    domain = "education"
    source = "GOV Website"
    source_url = "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem"
    license = "CC BY-ND 3.0 (the gov.br site's footer for its content; the microdata files state none of their own)"
    data_tags = ("Spatial",)
    download_description = """
        The microdata zips of the ENEM editions 2018 to 2023 from INEP's page "Microdados do Enem" (one zip per edition, 498 MB to 660 MB, each with DADOS/MICRODADOS_ENEM_<edition>.csv, ";"-separated, the dictionary in DICIONÁRIO/ and the Leia-me). The INEP server does not send its intermediate certificate (RNP ICPEdu GR46 OV TLS CA 2025, published by GlobalSign), so add it to the CA bundle, and it drops long connections, so resume with range requests. The definition reads the CSVs out of the zips.

        mkdir -p local-data-warehouse/enem_entrance_exam_scores/raw && cd local-data-warehouse/enem_entrance_exam_scores
        curl -sS http://secure.globalsign.com/cacert/rnpicpedugr46ovtlsca2025.crt | openssl x509 -inform der > rnp.pem
        cat /etc/ssl/certs/ca-certificates.crt rnp.pem > ca_bundle.pem
        for y in 2018 2019 2020 2021 2022 2023; do
          until curl -sS -C - --max-time 600 --cacert ca_bundle.pem -o raw/microdados_enem_$y.zip \\
            https://download.inep.gov.br/microdados/microdados_enem_$y.zip; do sleep 2; done
        done
        sha256sum raw/*.zip   # bytes and Last-Modified on 2026-11-09 after each sum
        # 2d582201180e70f6b4ff27bdb9e5f250766d724529cae9897fd21117b15d114b  2018: 657,874,840 (2022-05-23)
        # 88e66015749ed8660eccc326998b4475962daf0f5da325d1e962a9d792e1b801  2019: 659,560,141 (2022-05-23)
        # 3d462ff895d2066b8f8f8e20ee2cb65d72cb685b53d43a6ff0cd97f1521af608  2020: 620,776,982 (2022-02-16)
        # 0f5718493ed252569285a8a7f35be3c305f9bde15739a4eef3d0553fbee751ce  2021: 498,188,358 (2022-08-10)
        # 3cb321eb490fc4fd2d021fcd7672f1801a6ec37fdfea24a14369f054dc2d8faf  2022: 620,743,609 (2024-08-08)
        # 19512b7e29c9c8e940554396969722081341caa275c245a6c9d2d559c5d13a0a  2023: 549,511,687 (2026-07-09)
    """
    bibtex = r"""
        @misc{inep2026enem,
          author = {{Instituto Nacional de Estudos e Pesquisas Educacionais An{\'i}sio Teixeira (INEP)}},
          title = {Microdados do {Exame Nacional do Ensino M{\'e}dio} ({Enem}), edi{\c{c}}{\~o}es 2018 a 2023},
          year = {2026},
          howpublished = {\url{https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem}},
          note = {Bras{\'i}lia: INEP. One zip per edition; the 2023 zip as updated on 2026-07-09}
        }
    """
    curation_comments = """
        We start with the microdata files MICRODADOS_ENEM_<edition>.csv of the ENEM editions 2018 to 2023 from INEP (Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira): one row per registrant, 3.4 to 5.8 million registrants an edition, with the registration form, the socioeconomic questionnaire, the presence, the test versions, the answers and the scores.

        - Prediction point: the close of registration (May to July; the exam is in November, in 2020 in January and February 2021). For example, an NGO or a public cursinho programme (MEC's CPOP, whose cursinhos must prioritise Black, Indigenous and low-income students), or a state department filling limited places, asks its applicants the items of the registration form on its own intake form and ranks them by their expected mean score, to give its free preparation places. INEP holds the registration form and passes it only to MEC programmes and higher-education selection (Edital 30/2023, items 14.8 and 14.9), so the actor asks the same items itself; a department would also hold its students' grades and the state's assessment scores, which the data lack. INEP publishes the data for research and names no prediction: the use case is ours. USE-9 was asked: a direct use, such as a socioeconomic adjustment of schools' results, has its label known when it is made, so it is no prediction; the fit stays approximate. A mean of 450 points (with an essay above 0) is the threshold of ProUni scholarships and FIES loans; SISU admission weighs the five scores by course.
        - Rows: the registrants present at the four objective tests (TP_PRESENCA_* = 1), each with all five scores: 3,893,729 (2018), 3,701,909 (2019), 2,588,681 (2020), 2,238,107 (2021), 2,344,823 (2022) and 2,678,264 (2023), 45% (2020) to 73% (2019) of the registrants (decision 1). Absent and eliminated registrants have no score; one 2019 participant present at all four tests lacks a score and leaves. INEP removed the takers of 20 small adapted or reapplied test versions from the 2023 file (Leia-me 2023, section 3).
        - Selection bias: presence is unknown at registration and follows income and school status. In 2023, 61.8% of the registrants with a family income up to 1 minimum wage were present at all four tests against 81.7% above 4; 58.4% of those who had already finished secondary school against 82.5% of the treineiros. Treineiros (not finishing secondary school in the edition's year) are 17% to 19% of the rows (19.1% of 2023) and cannot use the edition for ProUni or FIES.
        - Target: `mean_score`, the mean of the four objective scores (IRT scales) and the essay (0 to 1000 in steps of 20). It keeps the zero INEP gives a test left entirely blank (16,167 natural-science and 16,302 mathematics zeros among 2023's 2,678,264 participants, every natural-science zero without an answer marked; in 2018 to 2022, 275 to 745 a year in natural sciences and in mathematics, 2,230 to 3,761 in humanities and 640 to 1,429 in languages) and an annulled essay (blank, copied, off topic: 3.5% of 2023's participants), as ProUni's mean does ("450 pontos de média nas notas das cinco provas", decision 2).
        - Anomaly: in 2023, 16,029 participants (0.60%) present on both days left both day-2 tests (natural sciences and mathematics) entirely blank, against 191 to 417 a year in 2018 to 2022; their mean score is 281. They are spread over every state (0.23% in RR to 1.33% in SC) and over the four regular booklets (0.60% to 0.62% each), graded like absence (state schools 0.67%, private schools 0.19%; the lowest income band 0.78%, band M 0.39%), and day-2 absence among day-1 participants fell by about as much (5.59% to 6.12% in 2018 to 2022, 5.04% in 2023), so they look like people earlier editions recorded absent on day 2, not a score recorded wrongly. INEP published their zeros and ProUni counts them, so they stay; a filter on blank answer strings would read the target's raw material. They are 0.6% of the 2023 test window and 6.3% of its squared error (untuned LightGBM, RMSE 76.10 with them, 73.89 without). Revisit if INEP documents a change in how it recorded day-2 presence in 2023.
        - Dropped as recorded on or after the exam days (LEAK-10): the presence (1 in every row after the filter), the test versions (CO_PROVA_*, which also code the adapted versions), the answer and key strings, the essay status and its five competence scores, and the five scores, the target's parts: no score of the same sitting is an input.
        - Not read: the registration number (a mask; "O mesmo NU_INSCRICAO para anos diferentes não identifica o mesmo participante", dictionary note 1), the state codes (copies of the state abbreviations), 2018's Q026 and Q027, asked that year only, and the school's operating status (TP_SIT_FUNC_ESC: it comes from a school census whose year neither the dictionaries nor the Leia-me give, so a school closed after the exam could show its later status; 0.17% of the rows have a school that is not active, and the column adds no measurable signal, LEAK-10).
        - Dropped `practice_only` (IN_TREINEIRO): from 2019 on, a "treineiro" is a registrant who had not finished secondary school and would not finish it in the edition's year (dictionary note 3), so the flag is 1 exactly when the school status is "completing after the edition's year" (every row of the 2019-2023 sample), a copy of that level (CLEAN-5); 2018 defined it by age as well (9,923 such registrants of the 2018 sample are not flagged), so it is not one scale across editions.
        - Edition codes (CLEAN-21): 2018 numbers the marital status from 0 (single) without "not informed"; we map it onto the codes of 2019 on. 2018's school type (TP_ESCOLA) is not the registrant's answer of the later editions but the administration of the school INEP matched (full 2018 file: code 2 is a state school on 840,241 of 840,392 rows, code 3, the dictionary's "abroad", a municipal school on 9,711 of 9,762, code 4 a private school on all 237,816, and code 1, "did not answer", every federal-school student and everyone without a matched school): we map state and municipal schools to public, private schools to private and a federal school to public; the other 2018 rows stay missing, and no 2018 row is abroad. The modality (TP_ENSINO) is filled for those finishing in the edition's year in every edition, and for about half of those already finished in 2018 and 2019 only; youth and adult education (EJA) occurs in 2018 only (7.2% of its known values; from 2019 the 1.9% to 5.4% of those finishing without a modality score like 2018's EJA students): we keep the modality for those finishing in the edition's year only and set 2018's EJA to missing, so the column means the same in every edition (regular or special education). The income bands are multiples of the year's minimum wage in every dictionary (R$ 954 in 2018 to R$ 1,320 in 2023), and we label them in minimum wages. TP_ANO_CONCLUIU counts years back from the edition to a last level "before 2007" (code 12 in 2018, 17 in 2023): we ship the years since the registrant finished secondary school, capped at "12 or more" in every edition, and missing for "not informed" (0), which is also the code of every registrant who has not finished.
        - Note: among those who have finished secondary school, "not informed" years since finishing rises from 2.5% (2018) and 3.2% (2019) to 8.1% to 10.9% (2020 to 2023), with the simplified layout of 2020; we cannot tell these registrants' years apart, so the shift stays.
        - Proxy missing values (CLEAN-10): marital status and nationality "not informed" (0), race "not declared" (0) and "does not have the information" (6, from 2021), the school type "did not answer" (1), and "I don't know" for the parents' schooling (H) and occupation (F).
        - Decoded into the dictionaries' words (CLEAN-12): the age bands, the parents' schooling and occupation groups (ordered in the dictionary, "grupos ordenados"), the income bands, the domestic worker's days and the counts of household goods ("4 or more" a level of its own) are ordered categories (CLEAN-14); the household size (1 to 20 people, as the form lists them) stays a number. The municipalities ship as "Name (UF) [code]", categories, from the names the same file gives each 7-digit IBGE code (NO_MUNICIPIO_ESC, NO_MUNICIPIO_PROVA): within an edition each code has one name and state and each name and state one code (checked in `_clean`); 13 codes changed their name between editions (a spelling, as "São Luís do Paraitinga" to "São Luiz do Paraitinga", or a new name, as "Augusto Severo" to "Campo Grande") and take the newest edition's name.
        - Note: the school items (municipality, state, administration, location) are filled only for registrants finishing secondary school in the edition's year whose school INEP identified: 66% (2020) to 89% (2018) of them, none of the others (73% of the rows are missing); the school type (TP_ESCOLA) is asked of those registrants only, so "did not answer" is missing for the others too, and the modality is kept for them only (edition codes).
        - Note: race, sex and family income are inputs, as on the registration form. The use case offers free preparation, a support offer and not a decision against the registrant, and Brazil's own admission policy (Lei 12.711/2012, the quota law) uses race and family income explicitly; the model is for that support only, not for screening anyone out (a merit scholarship, an admission, a hiring). Whether they stay is the curator's call (SEL-1; the Assam sibling `student_performance_on_an_entrance_examination` carries `Ethical Issue` for caste and gender).
        - Note: a registrant may sit several editions (to practise, then as a candidate, or again to improve), and the files cannot link them (dictionary note 1); a test participant may have an earlier row with a correlated score on the training side. That row is the person's own history, which a temporal split allows (LEAK-34), but the model cannot know it is theirs.
        - Anomaly: 2020 was held in January and February 2021, during the COVID-19 pandemic, with 55% of the registrants absent (2,588,681 participants of 5,783,109); it is a training edition only.
        - Duplicates kept (LEAK-18): 0.14% of the shipped rows share every input with another row (1,528 groups whose mean score varies by 47 points within a group: different people with the same coarse answers), and 0.03% to 0.04% of a test window's rows have a copy of their inputs (the edition aside) on its training side.
        - Spatial: the school's and the exam's municipality and state.
        - Note: the year is that of the pinned snapshot: the 2023 zip as re-published on 2026-07-09 (Last-Modified). The editions use the "modelo simplificado" INEP introduced with ENEM 2020 (Leia-me 2023, section 3: no school code, the age as a band, no municipality of birth or residence); 2018 and 2019 were re-published in it on 2022-05-23.
        - Note: the gov.br site publishes its content under CC BY-ND 3.0 (page footer); the microdata zips and their Leia-me state no licence of their own.
    """

    # Task
    target = "mean_score"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "INEP publishes the ENEM microdata for research and defines no prediction task or score; the microdata page "
            "and the Leia-me name none. Studies that predict ENEM scores from the microdata report several metrics "
            "(RMSE, MAE and R^2 together), none a deliberate single choice (MET-5); ProUni's 450-point threshold is an "
            "eligibility rule, not a threshold the source fixes for scoring a prediction (MET-6)."
        )
    )

    # Splits
    splits_comment = """
        We hold out each of the last 3 editions in turn (2023, 2022, 2021, newest first) and train on every earlier edition from 2018, as for a model refit once a year when the previous edition's scores are out (about January). No gap: the scores of edition t - 1 are published before the registration of edition t closes, and a refit from the public microdata gets edition t - 1 around the close of registration (later for 2020, held back under the LGPD); a one-edition gap would leave the 2021 window 43.5% of the participants for training. The history starts in 2018, so that the oldest window, 2021, trains on 58% of the participants (from 2019 it would be 46%, below the 50% floor). 2017 has the same questionnaire and is not read: the floor does not need it, and its essay scores sit on the level before the steps of 2019 and 2021 (mean 529 against 622 to 629 in the test editions). The training editions hold breaks the definition aligns or names (curation notes): 2018's school type comes from the matched school and is mapped onto public and private; 2018 and 2019 fill the modality for those already finished and 2018 alone has youth and adult education, both set to missing; "not informed" years since secondary school rise from 2020; the essay level steps up in 2019 and 2021. It holds the pandemic edition 2020 (held in January and February 2021, 55% absent); a refit would have trained on it too, and the test windows lie after it. Each test window keeps at most 500k of its participants, and each train side is a random 1M of the participants of the earlier editions (one random order for all windows); the frame is a uniform quarter of each edition (version comment).
    """
    temporal = Temporal(
        on="edition",
        splits=TemporalSplits(window=1, unit="unique", n_windows=3),
        horizon=1,
        horizon_unit="years",
    )
    row_budget = RowBudget(train=1_000_000, test=500_000)

    prepared_raw_files = (PREPARED, PREPARED_COUNTS)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # One pass over each edition's CSV (read out of its zip): keep the columns we read and the registrants present
        # at the four objective tests with all five scores, then draw a uniform SAMPLE_FRACTION of them.
        import zipfile

        import polars as pl

        columns = [*REGISTRATION, *MUNICIPALITY_NAMES.values(), *PRESENCE, *SCORES]
        frames, counts = [], []
        for edition in EDITIONS:
            with zipfile.ZipFile(raw_dir / ZIP.format(edition=edition)) as archive:
                (member,) = [n for n in archive.namelist() if n.endswith(MEMBER.format(edition=edition))]
                # every edition's CSV is Latin-1 (the municipality names); polars reads UTF-8
                data = archive.read(member).decode("latin-1").encode("utf-8")
            frame = pl.read_csv(data, separator=";", infer_schema=False, columns=columns)
            del data
            present = frame.filter(pl.all_horizontal([pl.col(c) == "1" for c in PRESENCE]))
            scored = present.filter(pl.all_horizontal([pl.col(c).is_not_null() for c in SCORES]))
            rng = np.random.default_rng(SAMPLE_SEED + edition)
            rows = np.sort(rng.choice(scored.height, size=round(SAMPLE_FRACTION * scored.height), replace=False))
            counts.append(
                {
                    "edition": edition,
                    "registrants": frame.height,
                    "present_at_all_four_tests": present.height,
                    "with_all_five_scores": scored.height,
                    "sampled": len(rows),
                }
            )
            frames.append(scored[rows].drop(PRESENCE))
            del frame, present, scored
        pl.concat(frames, how="vertical").write_parquet(raw_dir / PREPARED, compression="zstd")
        pd.DataFrame(counts).to_csv(raw_dir / PREPARED_COUNTS, index=False)

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {"participants": pd.read_parquet(raw_dir / PREPARED), "counts": pd.read_csv(raw_dir / PREPARED_COUNTS)}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df = raw["participants"].rename(columns=REGISTRATION)
        # 1. The target: the mean of the five scores, with the zero of a blank test or an annulled essay.
        df[self.target] = df[list(SCORES)].astype(float).mean(axis=1)
        df = drop_columns(df, SCORES)
        df["edition"] = df["edition"].astype("int16")
        # 2. 2018's codes onto those of 2019 on: the marital status from 0; the school type from the matched school's
        #    administration (a federal school is public, the other "did not answer" stay missing).
        y2018 = df["edition"] == 2018
        df.loc[y2018, "marital_status"] = df.loc[y2018, "marital_status"].replace(MARITAL_2018)
        school_type = df.loc[y2018, "secondary_school_type"]
        federal = (school_type == "1") & (df.loc[y2018, "school_administration"] == SCHOOL_TYPE_FEDERAL)
        df.loc[y2018, "secondary_school_type"] = school_type.map(SCHOOL_TYPE_2018).mask(federal, "2")
        #    The modality only for those finishing in the edition's year, as every edition records it, without
        #    2018's youth and adult education.
        modality = df["secondary_school_modality"]
        finishing = df["secondary_school_status"] == FINISHING_THIS_YEAR
        df["secondary_school_modality"] = modality.where(finishing & (modality != EJA))
        # 3. Years since finishing secondary school: the code counts back from the edition, capped at
        #    YEARS_SINCE_CAP; 0 is "not informed", the code of everyone who has not finished.
        years = pd.to_numeric(df["years_since_secondary"]).astype("int16")
        capped = years.clip(upper=YEARS_SINCE_CAP).astype(str).replace({str(YEARS_SINCE_CAP): YEARS_SINCE_LEVELS[-1]})
        df["years_since_secondary"] = capped.where(years > 0)
        # 4. `practice_only` copies a level of the school status from 2019 on (dictionary note 3): drop it.
        df = drop_columns(df, ["practice_only"])
        # 5. Proxy missing values, then the dictionaries' words; the municipalities as "Name (UF) [code]".
        for col, codes in PROXY_MISSING.items():
            df[col] = df[col].mask(df[col].isin(codes))
        df = _decode_codes(df, CODE_LABELS)
        for col, name_col in MUNICIPALITY_NAMES.items():
            df[col] = _municipality_labels(df, col, name_col, col.replace("municipality", "state"))
        df = drop_columns(df, list(MUNICIPALITY_NAMES.values()))
        df["household_size"] = pd.to_numeric(df["household_size"]).astype("float32")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=CATEGORICAL, ordinal=ORDINAL)

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        counts = raw["counts"].copy()
        counts["share of registrants"] = (counts["with_all_five_scores"] / counts["registrants"]).round(3)
        p = raw["participants"]
        edition = p["NU_ANO"].rename("edition")
        scores = p[list(SCORES)].astype(float)
        target = (scores == 0).groupby(edition).mean().round(4)
        target.columns = [f"share zero {c.removeprefix('NU_NOTA_').lower()}" for c in SCORES]
        mean = scores.mean(axis=1)
        for q in (0.1, 0.5, 0.9):
            target[f"mean score p{round(q * 100)}"] = mean.groupby(edition).quantile(q).round(1)
        target["share below 450"] = (mean < 450).groupby(edition).mean().round(3)
        return [
            Decision(
                "Participants per edition",
                "The rows are the registrants present at the four objective tests, all with five scores; "
                "`_prepare_raw_files` keeps a uniform quarter of each edition.",
                counts,
            ),
            Decision(
                "The target: the mean of the five scores",
                "The share of zero scores (a test left blank, an annulled essay) in the sample, and the mean score's "
                "quantiles and share below ProUni's 450 points, by edition.",
                target,
            ),
        ]
