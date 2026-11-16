"""Curated dataset definition for `sinan_dengue_case_screening_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
    drop_columns,
    set_missing,
)

# The yearly files whose notifications include the discarded cases: the open files of 2014-2015 and 2022-2026 hold only
# probable cases (no `CLASSI_FIN` = 5), so they have no negative class (measured on the files of 2026-11-07).
YEARS = (2016, 2017, 2018, 2019, 2020, 2021)
PREPARED = "sinan_dengue_lab_criterion_2016_2021.parquet"

# The final classification (`CLASSI_FIN`) of the dengue form since 2014 (5 discarded; 10 dengue, 11 dengue with alarm
# signs, 12 severe dengue) and the codes of the older form still on a few 2016 rows (1-4, all confirmed dengue).
# 8 (inconclusive) and blank carry no decision and leave the cohort.
DENGUE_CODES = ("1", "2", "3", "4", "10", "11", "12")
DISCARDED_CODE = "5"
# The collection dates of the dengue samples (IgM serology, NS1 antigen, RT-PCR, viral isolation; dictionary fields
# 45-53): a sample dated before the notification date was taken before the prediction point.
SAMPLE_DATES = ("DT_SORO", "DT_NS1", "DT_PCR", "DT_VIRAL")

# Clinical signs (1 yes, 2 no) and pre-existing diseases (1 yes, 2 no, 9 unknown) of the form's clinical section,
# renamed to English (data dictionary of 14/07/2025, fields 24-44).
SIGNS = {
    "FEBRE": "fever",
    "MIALGIA": "myalgia",
    "CEFALEIA": "headache",
    "EXANTEMA": "rash",
    "VOMITO": "vomiting",
    "NAUSEA": "nausea",
    "DOR_COSTAS": "back_pain",
    "CONJUNTVIT": "conjunctivitis",
    "ARTRITE": "arthritis",
    "ARTRALGIA": "severe_arthralgia",
    "PETEQUIA_N": "petechiae",
    "LEUCOPENIA": "leukopenia",
    "LACO": "tourniquet_test_positive",
    "DOR_RETRO": "retro_orbital_pain",
}
COMORBIDITIES = {
    "DIABETES": "diabetes",
    "HEMATOLOG": "hematologic_disease",
    "HEPATOPAT": "liver_disease",
    "RENAL": "chronic_kidney_disease",
    "HIPERTENSA": "hypertension",
    "ACIDO_PEPT": "acid_peptic_disease",
    "AUTO_IMUNE": "autoimmune_disease",
}
PLACES = {
    "SG_UF_NOT": "notification_state",
    "ID_MUNICIP": "notification_municipality",
    "ID_REGIONA": "notification_health_region",
    "ID_UNIDADE": "notifying_unit",
    "SG_UF": "residence_state",
    "ID_MN_RESI": "residence_municipality",
    "ID_RG_RESI": "residence_health_region",
    "ID_PAIS": "residence_country",
}
PERSON = {
    "CS_SEXO": "sex",
    "CS_GESTANT": "pregnancy",
    "CS_RACA": "race_colour",
    "CS_ESCOL_N": "schooling",
    "ID_OCUPA_N": "occupation_cbo",
}

# IBGE state codes (the dictionary's "Tabela com Códigos e siglas padronizados pelo IBGE").
IBGE_STATES = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP", "17": "TO",
    "21": "MA", "22": "PI", "23": "CE", "24": "RN", "25": "PB", "26": "PE", "27": "AL", "28": "SE", "29": "BA",
    "31": "MG", "32": "ES", "33": "RJ", "35": "SP", "41": "PR", "42": "SC", "43": "RS",
    "50": "MS", "51": "MT", "52": "GO", "53": "DF",
}  # fmt: skip
SCHOOLING_LEVELS = [
    "illiterate",
    "primary grades 1-4 incomplete",
    "primary grade 4 complete",
    "primary grades 5-8 incomplete",
    "primary complete",
    "secondary incomplete",
    "secondary complete",
    "higher education incomplete",
    "higher education complete",
]
CODE_LABELS = {
    **{c: {"1": "Yes", "2": "No"} for c in SIGNS.values()},
    **{c: {"1": "Yes", "2": "No"} for c in COMORBIDITIES.values()},
    "sex": {"M": "male", "F": "female"},
    "pregnancy": {
        "1": "1st trimester",
        "2": "2nd trimester",
        "3": "3rd trimester",
        "4": "gestational age unknown",
        "5": "not pregnant",
        "6": "not applicable",
    },
    "race_colour": {"1": "white", "2": "black", "3": "yellow", "4": "brown", "5": "indigenous"},
    "schooling": dict(zip(["0", "1", "2", "3", "4", "5", "6", "7", "8"], SCHOOLING_LEVELS, strict=True)),
    "notification_state": IBGE_STATES,
    "residence_state": IBGE_STATES,
}
# SINAN's own occupation codes outside the CBO, in its occupation table (DATASUS TabWin file OCUPANET.cnv in
# TAB_SINANNET.zip, ftp.datasus.gov.br/dissemin/publicos/SINAN/AUXILIAR/; `semocupa.cnv` lists the same five).
SINAN_OCCUPATIONS = {
    "999991": "student [999991]",
    "999992": "homemaker [999992]",
    "999993": "retired or pensioner [999993]",
    "999994": "chronically unemployed or usual occupation not obtained [999994]",
    "999995": "prisoner [999995]",
}
# Codes that mean unknown or blank (the export writes a blank field as "" or "0"); the occupation table names "XXX"
# "not informed", 998999 "ignored" and 000000 "CBO without definition"; 10 of schooling is "not applicable" (under 7
# years), a state off the scale, so missing (CLEAN-14).
MISSING_CODES = {
    **{c: [""] for c in SIGNS.values()},
    **{c: ["", "9"] for c in COMORBIDITIES.values()},
    "sex": ["", "I"],
    "pregnancy": ["", "9"],
    "race_colour": ["", "9"],
    "schooling": ["", "9", "09", "10"],
    "occupation_cbo": ["", "0", "XXX", "000000", "998999"],
    "notifying_unit": [""],
    "notification_health_region": ["", "0"],
    "residence_health_region": ["", "0"],
    "residence_state": [""],
    "residence_municipality": [""],
    "residence_country": [""],
}

# Columns filled after the notification or that encode the outcome (dictionary fields 22 and 45-115); dropped
# (LEAK-10). The laboratory results and their dates decide the label.
POST_NOTIFICATION = [
    "DT_INVEST",  # date the investigation started
    *["DT_CHIK_S1", "DT_CHIK_S2", "DT_PRNT", "RES_CHIKS1", "RES_CHIKS2", "RESUL_PRNT"],  # chikungunya serology
    *["DT_SORO", "RESUL_SORO", "DT_NS1", "RESUL_NS1", "DT_VIRAL", "RESUL_VI_N", "DT_PCR", "RESUL_PCR_"],  # dengue tests
    *["SOROTIPO", "HISTOPA_N", "IMUNOH_N"],  # serotype, histopathology, immunohistochemistry
    *["HOSPITALIZ", "DT_INTERNA", "UF", "MUNICIPIO"],  # hospitalisation, its date and place
    *["TPAUTOCTO", "COUFINF", "COPAISINF", "COMUNINF", "DOENCA_TRA"],  # filled for confirmed cases, erased if discarded
    *["CLASSI_FIN", "CRITERIO", "CLINC_CHIK", "EVOLUCAO", "DT_OBITO", "DT_ENCERRA"],  # outcome and closing
    *[f"ALRM_{s}" for s in ("HIPOT", "PLAQ", "VOM", "SANG", "HEMAT", "ABDOM", "LETAR", "HEPAT", "LIQ")],
    "DT_ALRM",  # alarm signs: filled only for classification 11 (dengue with alarm signs) or 12
    *[
        f"GRAV_{s}"
        for s in (
            "PULSO",
            "CONV",
            "ENCH",
            "INSUF",
            "TAQUI",
            "EXTRE",
            "HIPOT",
            "HEMAT",
            "MELEN",
            "METRO",
            "SANG",
            "AST",
            "MIOC",
            "CONSC",
            "ORGAO",
        )
    ],
    "DT_GRAV",  # severity signs: filled only for classification 12 (severe dengue)
    *["MANI_HEMOR", "EPISTAXE", "GENGIVO", "METRO", "PETEQUIAS", "HEMATURA", "SANGRAM", "LACO_N", "PLASMATICO"],
    *["EVIDENCIA", "PLAQ_MENOR", "CON_FHD", "COMPLICA"],  # the older form's haemorrhagic-fever section (empty)
]
SYSTEM = [
    "TP_NOT",  # notification type: individual on all but a handful of rows
    "ID_AGRAVO",  # A90 (dengue) on every row
    "SEM_NOT",  # epidemiological week and year of the notification date
    "NU_ANO",
    "SEM_PRI",  # epidemiological week of the onset date
    "DT_SIN_PRI",  # onset date: kept as the days from onset to notification
    "NU_IDADE_N",  # coded age: kept as age_years
    "DT_NASC",  # birth date (2016-2019 files) and birth year (2020-2021): personal data, the age is kept
    "ANO_NASC",
    *["TP_SISTEMA", "NDUPLIC_N", "DT_DIGITA", "CS_FLXRET", "FLXRECEBI", "MIGRADO_W"],  # system fields
    "source_year",  # the yearly file a row came from
]


class SinanDengueCaseScreening1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Is a suspected dengue case notified in Brazil confirmed as dengue by the laboratory, or discarded, "
            "judged from the symptoms, the patient and the place at notification?"
        ),
        use_case=(
            "The municipal surveillance team, when a suspected dengue case is notified and before the dengue test's "
            "result, estimates whether it is dengue: to close the notifications never tested, on clinical and "
            "epidemiological grounds (Ministry of Health manual, 2016, 8.4-8.5), and to choose whom to test. A "
            "physician may read it for the differential diagnosis (Bohm et al. 2024: 'to assist in "
            "medical decision-making based only on clinical data')."
        ),
        row=(
            "One notification of suspected dengue to SINAN, Brazil's national surveillance system, from 2016 to "
            "2021, among those the laboratory decided and with no dengue sample taken before the notification day: "
            "2.25 million notifications with the form's clinical section."
        ),
        predicted=(
            "Whether the case was closed as dengue (with or without alarm signs, or severe) by a laboratory result, "
            "rather than discarded; decided days to weeks after notification."
        ),
        known=(
            "The date and place of notification and residence, the notifying unit, age, sex, pregnancy, race or "
            "colour, schooling, occupation, the days since the first symptoms, 14 clinical signs (fever, rash, "
            "a tourniquet test, leukopenia when a blood count was done) and 7 pre-existing diseases."
        ),
        split=(
            "Each test window is a later half-year (July 2020 to December 2021, the COVID-19 years), and training "
            "stops one month before it, as for a model refit twice a year once most earlier cases are closed."
        ),
        changes=(
            "We keep only the notifications decided by a laboratory, drop those made after a dengue sample was "
            "already taken (14%), drop every field filled during or after the investigation, and drop the rows "
            "without the clinical section (most of early 2016)."
        ),
        fit="approximate",
        fit_reason=(
            "The inputs are those of the notification, but only the cases a laboratory decided carry a reliable "
            "label, while the team decides on the untested ones: 42% of the decided notifications of 2016-2021 were "
            "tested (47.7% dengue, against 64.0% among the clinical closings), fewer at a state's epidemic peaks "
            "(40.3% against 50.6% off-peak), and 56% in 2021 against 37-42% before (notes)."
        ),
    )

    # Dataset
    unique_name = "sinan_dengue_case_screening_1m"
    version_of = "sinan_dengue_case_screening"
    version_comment = """
        We sample per test window (v2 split protocol): each half-year window keeps at most 500k of its rows (all three fit whole), and each train side is a random 1M of all rows notified before the window minus the one-month gap (1.68M to 2.11M rows), drawn in one random order for all windows; the frame keeps only the rows a split uses.
    """
    year = "2023"
    domain = "medical & healthcare"
    source = "GOV Website"
    source_url = "https://dadosabertos.saude.gov.br/dataset/arboviroses-dengue"
    license = "CC BY-ND 3.0"
    data_tags = ("Spatial",)
    download_description = """
        We download the yearly CSV files of 2016-2021 and the data dictionary from the Ministry of Health's open-data portal (Portal de Dados Abertos do SUS, dataset "Sinan/Dengue"). The files are replaced weekly, the old years included, so a later download may differ: ours were last modified on 2026-10-01 (2016) and 2026-11-07 (2017-2021), with these SHA-256 sums: DENGBR16 635b9fbd..., DENGBR17 53ac88a9..., DENGBR18 8c40e901..., DENGBR19 204a68f2..., DENGBR20 2ed5ba9f..., DENGBR21 d7c8a5b3... (first 8 hex digits).

        mkdir -p local-data-warehouse/sinan_dengue_case_screening && cd local-data-warehouse/sinan_dengue_case_screening
        for y in 16 17 18 19 20 21; do wget https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Dengue/csv/DENGBR$y.csv.zip; done
        wget https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINAN/Dengue/dic_dados_dengue.pdf
    """
    bibtex = """
        @misc{ministeriodasaude2023sinandengue,
          author = {{Minist{\\'e}rio da Sa{\\'u}de}},
          title = {Sinan/Dengue: notifica{\\c{c}}{\\~o}es de dengue, 2000-2026},
          howpublished = {DATASUS, \\url{ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/DADOS/FINAIS/}; Portal de Dados Abertos do SUS, \\url{https://dadosabertos.saude.gov.br/dataset/arboviroses-dengue}},
          year = {2023},
          note = {Coordena{\\c{c}}{\\~a}o-Geral de Vigil{\\^a}ncia de Arboviroses and Coordena{\\c{c}}{\\~a}o-Geral de Informa{\\c{c}}{\\~o}es e An{\\'a}lises Epidemiol{\\'o}gicas (SVSA). Files of 2026-11-07},
        }
    """
    curation_comments = """
        We start with the yearly files DENGBR16 to DENGBR21 (CSV) of the Ministry of Health's "Sinan/Dengue" dataset on the Portal de Dados Abertos do SUS, with its data dictionary of 14/07/2025.

        - Prediction point: the notification of a suspected case at a health unit (the notification date), before the dengue test's result. Only what the form's notification, patient, residence and clinical sections hold then is a feature: the investigation starts on the notification day for 93% of the rows (`DT_INVEST`), and the clinical section is filled with it.
        - Use case: the municipal surveillance team closes the notifications that are never tested on clinical and epidemiological grounds (in an epidemic every case but the first of an area; a case compatible with another disease is discarded) and chooses whom to test (Ministério da Saúde, "Dengue: diagnóstico e manejo clínico", 5th ed. 2016, 8.4-8.5). The physician's differential diagnosis is a second reading. USE-9 was asked: a physician who has sent a sample and waits for its result would meet this cohort, but the 2016 protocol manages every suspected case by its risk group whatever the confirmation, so that actor takes no decision on the score, and the fit stays approximate.
        - History: the target needs the discarded cases, and only the files of 2016-2021 hold them. The open files of 2014-2015 and 2022-2026 hold probable cases only (no `CLASSI_FIN` = 5 among their 0.47M to 6.6M rows a year; the portal defines probable cases as every notified suspected case except the discarded ones), so the 6.5M notifications of 2024 the screening counted cannot be labelled. Files before 2014 use the older form without the clinical signs. We keep the notifications dated 2016-2021 (683 rows of these files dated outside them dropped).
        - Cohort: the notifications a laboratory decided (`CRITERIO` = 1; read in `_prepare_raw_files`), as in Bohm et al. 2024: 2,979,887 of the 7,030,293 notifications of 2016-2021 that were confirmed or discarded (42%; 35% of the confirmed cases, 48% to 56% of the discarded ones, by year). The clinical-epidemiological closings carry no laboratory decision and are left out, as are the inconclusive (code 8) and open rows. Training on them would teach the team's own closing habits.
        - Selection (USE-8, `Selection Bias`): the team decides on the untested notifications, which this cohort does not hold. Among the decided notifications of 2016-2021, the laboratory closings are 47.7% dengue and the clinical-epidemiological ones 64.0%; the laboratory share is 40.3% in a state's busiest months against 50.6% in its quietest, so the tested cases come more often from outside epidemic peaks. The share rises from 37% to 42% of the decided notifications in 2016-2019 (training) to 46% in 2020 and 56% in 2021 (test), and in 2021 the tested cases are for the first time more often dengue than the clinical closings (2021Q1 46.7% against 45.3%, 2021Q2 55.7% against 50.8%), so the direction of the gap changes inside the test period.
        - Target: `dengue_confirmed` is "Yes" for the final classifications dengue (10), dengue with alarm signs (11) and severe dengue (12), and for the older form's codes 1-4 still on a few 2016 rows (all confirmed dengue in that form), "No" for discarded (5); 45% "Yes" overall, from 12% to 56% by quarter (the off-season holds more discarded cases). The label is a conclusive laboratory result on 92.4% of the rows of each class (a positive test for "Yes", a negative and no positive for "No"). "No" means a negative test, not the absence of dengue: IgM is reliable from the sixth day of symptoms and NS1 up to the fifth (manual, section 7), so the label's noise depends on the days since onset, a kept input.
        - Rows without the form's clinical section (all 14 signs and 7 diseases blank) are no task rows (USE-7): 355,366 rows, nearly all of January to June 2016, when the clinical fields first came into use (78% of the January 2016 rows blank, under 1% from July 2016 on). With them go the older-form rows of 2016.
        - Notified after a dengue sample was taken (USE-3): 370,314 of the remaining 2,623,839 rows (14.1%; 12.6% to 16.0% of each test window) have an IgM, NS1, RT-PCR or isolation sample dated before the notification date, 100,893 of them more than a week before. These notifications often follow the result (an NS1 taken before notification is positive in 51% of them against 35% when taken on the notification day; 61.7% dengue against 45.1% in the rows kept), so they are past the prediction point. The features found them (ROC AUC 0.87 to 0.90 for "sampled before notification", through the notifying unit and the days since onset) and lifted the score by 0.004 to 0.031 (LightGBM, column auditor). We drop them by the collection dates, facts dated before the notification, so the filter reads no label (as the input-based cuts of nyc_taxi_trip_duration_1m and pkdd_15). The 1,148,649 rows kept (51%) whose sample was taken on the notification day stay: whether a same-day NS1 result was in hand cannot be told from the data.
        - Dropped as filled after the notification or set by the outcome (LEAK-10, LEAK-2; dictionary fields 22 and 45-115): the investigation date; every laboratory test and its date (dengue IgM, NS1, viral isolation, RT-PCR, serotype, histopathology, immunohistochemistry; chikungunya serology and PRNT; the dengue sample dates are read only for the filter above); hospitalisation, its date and place; the place of infection and the work-relatedness (`TPAUTOCTO`, `COUFINF`, `COPAISINF`, `COMUNINF`, `DOENCA_TRA`), which the system fills for confirmed cases and erases when a case is discarded (the four place fields blank for 98% to 99% of the discarded rows against 20% to 25% of the confirmed ones); the final classification, criterion, chikungunya presentation, evolution, death and closing dates; the alarm and severity signs with their dates, enabled only for classifications 11 and 12; and the older form's haemorrhagic-fever fields (blank on nearly every kept row).
        - Dropped as system or derived fields: the notification type and disease code (constant), the epidemiological weeks and year (from the dates), the system type, the duplicate mark, the typing date and the return-flow fields; the birth date (2016-2019) and birth year (2020-2021) as personal data, the age kept.
        - Built: `age_years` from the coded age (its first digit the unit: hours, days, months, years; ages over 120 missing) and `days_onset_to_notification` from the onset date (median 3 days; set missing beyond 365 days, a mistyped year, 4,688 rows). The notification date stays as a datetime and the task's time column.
        - Codes decoded into the dictionary's words (CLEAN-12): the 14 signs and 7 diseases (Yes, No; 9 "ignorado" missing), sex (I missing), pregnancy, race or colour (9 missing), the IBGE state codes into their abbreviations, and schooling as an ordered category from illiterate to higher education complete (9 and blank missing; 10 "not applicable", under 7 years, missing as a state off the scale, CLEAN-14). Municipality, health region, notifying unit (CNES) and country stay categorical codes, an entity's or a place's code whose name is a copy of the id.
        - Occupation: the dictionary points to SINAN's occupation table (CBO 2002 plus SINAN's own codes), which DATASUS distributes as the TabWin file `OCUPANET.cnv` (`TAB_SINANNET.zip`, SINAN/AUXILIAR on its FTP server). SINAN's own codes outside the CBO get the table's words: student, homemaker, retired or pensioner, chronically unemployed or usual occupation not obtained, and prisoner (402,995 rows, 17.9%). The table's codes for unknown are missing: "XXX" (not informed), 998999 (ignored, 62,397 rows) and 000000 (CBO without definition, 7,452 rows), as are "0" and blank (65% of the rows missing in all). The CBO codes stay codes (open for the curator, together with rais_employment_separation's CBO). 1,280 rows coded 10001 and 241 coded 999990 are in no table and stay as published.
        - Note: leukopenia is a blood-count finding, listed by the form among the clinical signs (field 35, not in the laboratory section); it is known at notification only when a count was done at the first visit, which the 2016 protocol requires for risk group B, and the form has no "not done", so "No" mostly means no count (5.7% "Yes"). Its association with the label does not grow when the section may have been filled later (odds ratio 2.28 with the investigation on the notification day, 2.94 one to seven days later, 2.91 later still), and the 2021 forms first typed after closing carry no more clinical signal than those typed before (ROC AUC on the clinical inputs 0.635 against 0.639). It stays: dengue in 65% of the rows with it, 44% without, and dropping it costs ROC AUC 0.0025 (LightGBM on 300k training rows, the three windows: 0.705 against 0.703, lower on 1 of 3 windows by 0.009 and within 0.001 on the others).
        - Note: the notifying unit alone scores ROC AUC 0.637 against 0.686 for all features (leak probe 2), and 0.677 without it (probe 1); the seven place columns together are worth about 0.10 (LightGBM, 0.705 against 0.608 without them): a unit's place and case mix, known when it notifies. Its rows are the unit's own history, legitimate under a temporal split (LEAK-34). Within one notifying unit and month the model ranks cases at ROC AUC 0.59 to 0.62 (domain practitioner, before the filter), about what the WHO clinical case definition achieves.
        - Exact copies over every input kept as natural repeats (LEAK-18): 4,541 rows (0.2%) in 2,237 groups share the date, unit, places, age in years and every finding. Where the 2016-2019 files give a birth date on every copy, 815 of 1,367 groups are different patients (other birth dates) and 552 one patient notified twice; the 264 groups with both labels are mostly different patients (129 of 160 with birth dates), a label ambiguity the task has (LEAK-20). The copies of one patient stay as an exception to LEAK-19, which drops copies of one entity (proposed by the review panel, 2026-11-09, for the curator to confirm): the notification date is an input, so no copy over every input crosses the split, and in the test years 2020-2021 (birth year only) they cannot be told apart from different patients. Leak probe 5: 0.6% of the test rows (0.5% to 0.7% per window) match a training row on every input but the date; none with it.
        - Anomaly: Espírito Santo notified through e-SUS Vigilância em Saúde from 2020 (the portal's note), so its rows fall from 16,923 in 2019 to 444 in 2020 and 6,748 in 2021 (before the pre-notification filter); kept as published.
        - Year: 2023 at the latest. DATASUS distributes the same yearly files on its FTP server (dissemin/publicos/SINAN/DADOS/FINAIS; its DENGBR23.dbc holds the portal's 1,645,956 rows of 2023), and Bohm et al. took these data "available in DataSUS" before submitting on 28 November 2023; the files are overwritten, so an earlier first upload cannot be read. The portal's dataset page dates from 22 February 2024.
        - Licence: the portal states Creative Commons Atribuição-SemDerivações 3.0 (CC BY-ND 3.0), a note for the release checklist (EV-4).
    """

    # Task
    target = "dengue_confirmed"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Bohm et al. 2024 (BMC Public Health 24:1573) define accuracy, sensitivity, specificity, precision and F1 "
            "(Table 4) and ROC AUC in the text, name the decision tree best on accuracy and F1 and the MLP on AUC, and "
            "pick the tree as a compromise with computational cost: no single criterion (MET-5). Their call for high "
            "sensitivity fixes no threshold or cost (MET-6), and the SINAN portal and dictionary define no metric. "
            "Fallback ROC AUC on the probabilities (MET-8): the team ranks cases to close and to test. Log loss is set "
            "aside: the dengue share swings from 12% to 56% by quarter, and the untuned families' log loss sits near or "
            "above the constant's (0.655 to 0.943 against 0.673), so it would mostly test the shift of the base rate."
        )
    )

    # Splits
    splits_comment = """
        A model built on past seasons scores the next cases, refit twice a year. Test windows are the last three half-years of the labelled period (July-December 2021, January-June 2021, July-December 2020; 108k, 345k and 88k rows, 31.5%, 49.7% and 23.3% dengue, smallest class 20,501), newest first. Yearly windows would leave only two windows whose train side holds half the rows (SPLIT-14): 2019 to 2021 hold 73% of them. Each train side is everything notified up to one month before its window (1.68M to 2.11M rows, 74% to 93%), a random 1M of them. The gap: a case is closed a median 13 to 20 days after its notification (90% within 48 to 61 days; confirmed and discarded cases alike, 17 against 18 days), so a refit at a window's start knows most labels of the month before it; with no gap 0.5% to 1.8% of the training rows were still open at the window start, with one month 0.14% to 0.85%. A two-month gap cost 0.026 to 0.037 ROC AUC on the July windows against training on every label closed by the start (LightGBM, before the pre-notification filter), and a one month gap recovers 58% to 100% of it.
        Seasons: January-June, the dengue season, holds 67% to 84% of a year's notifications, but two of the three windows are the July-December off-season. They hold 36% of the test rows and two thirds of the weight in the mean over windows, and they score higher (random forest 0.76 and 0.73 against 0.63 in season, task probe), so the mean over windows sits above the row-weighted mean (0.708 against 0.674). The order of the model families measured before the filter is the same in every window (LightGBM over logistic regression by 0.058 to 0.084).
        COVID-19: all three windows follow its arrival in Brazil (March 2020), and no labelled year after 2021 exists (the open files of 2022 on hold no discarded case). Measured breaks: the laboratory share of the confirmed cases rose from 0.20-0.32 (2016H2-2019H2) to 0.40-0.60, fever "Yes" fell from 0.80-0.86 to 0.73-0.77 and leukopenia "Yes" halved (0.07-0.08 to 0.04); the training history holds four seasons before it.
        Protocol: the data holds the labelled rows of the month between a train side's end and its window; they are outside the training indices, and a participant must not train on them (their labels were not all known at the window start). Counting a municipality's or a unit's notifications inside a test window reads the test rows' own features after each row (about +0.006 ROC AUC, measured by the task gamer); no shipped column carries it, and a deployed model that scores cases as they arrive does not have it. Each window keeps all its rows (under the 500k test budget).
    """
    temporal = Temporal(
        on="notification_date",
        splits=TemporalSplits(window=6, unit="months", n_windows=3, gap=1),
    )
    row_budget = RowBudget(train=1_000_000, test=500_000)

    prepared_raw_files = (PREPARED,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # The six yearly CSVs (8.1M notifications, 2.2 GB unzipped) are read in blocks as text, and only the
        # notifications closed on the laboratory criterion (`CRITERIO` = 1) are kept, every column as published.
        import pyarrow as pa
        import pyarrow.compute as pc
        import pyarrow.csv as pacsv
        import pyarrow.parquet as pq

        tables = []
        for year in YEARS:
            with zipfile.ZipFile(raw_dir / f"DENGBR{year % 100:02d}.csv.zip") as archive:
                (name,) = archive.namelist()
                with archive.open(name) as f:
                    header = f.readline().decode().strip().split(",")
                with archive.open(name) as f:
                    reader = pacsv.open_csv(
                        f,
                        read_options=pacsv.ReadOptions(block_size=64 << 20, use_threads=False),
                        convert_options=pacsv.ConvertOptions(column_types=dict.fromkeys(header, pa.string())),
                    )
                    batches = [batch.filter(pc.equal(batch.column("CRITERIO"), "1")) for batch in reader]
            table = pa.Table.from_batches(batches)
            table = table.append_column("source_year", pa.array([str(year)] * table.num_rows, pa.string()))
            tables.append(table)
        pq.write_table(pa.concat_tables(tables, promote_options="default"), raw_dir / PREPARED)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        import pyarrow.parquet as pq

        return pq.read_table(raw_dir / PREPARED).to_pandas()

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # 1. The cohort: notifications of 2016-2021 that a laboratory decided as dengue or discarded.
        df["notification_date"] = pd.to_datetime(df["DT_NOTIFIC"], format="%Y-%m-%d")
        df = df[df["notification_date"].dt.year.between(YEARS[0], YEARS[-1])]
        df = df[df["CLASSI_FIN"].isin([*DENGUE_CODES, DISCARDED_CODE])]
        df[self.target] = np.where(df["CLASSI_FIN"] == DISCARDED_CODE, "No", "Yes")
        # 2. Rows without the clinical section (the form's signs and diseases all blank) are no task rows (USE-7).
        empty = df[list(SIGNS) + list(COMORBIDITIES)].fillna("").isin(["", "0"]).all(axis=1)
        df = df[~empty]
        # 3. Notifications made after a dengue sample was collected are past the prediction point (USE-3): the
        #    collection dates are facts dated before the notification, so the filter reads no label.
        sampled = pd.concat(
            [pd.to_datetime(df[c], format="%Y-%m-%d", errors="coerce") for c in SAMPLE_DATES], axis=1
        ).min(axis=1)
        df = df[~(sampled < df["notification_date"])]
        # 4. Age in years from the coded age (first digit the unit: 1 hours, 2 days, 3 months, 4 years).
        age = pd.to_numeric(df["NU_IDADE_N"], errors="coerce")
        scale = (age // 1000).map({1: 1 / 8766, 2: 1 / 365.25, 3: 1 / 12, 4: 1.0})
        df["age_years"] = ((age % 1000) * scale).where(lambda a: a <= 120)
        # 5. Days from the first symptoms to the notification; over a year is a recording error (a mistyped year).
        onset = pd.to_datetime(df["DT_SIN_PRI"], format="%Y-%m-%d", errors="coerce")
        lag = (df["notification_date"] - onset).dt.days
        df["days_onset_to_notification"] = lag.where(lag.between(0, 365))
        # 6. Drop the post-notification and system fields, then rename to English and decode the codes; the CBO
        #    occupation codes stay codes, SINAN's own codes outside the CBO get their words.
        df = drop_columns(df, ["DT_NOTIFIC", *POST_NOTIFICATION, *SYSTEM])
        df = df.rename(columns={**SIGNS, **COMORBIDITIES, **PLACES, **PERSON})
        df = set_missing(df, MISSING_CODES)
        df = decode(df, CODE_LABELS)
        df["occupation_cbo"] = df["occupation_cbo"].replace(SINAN_OCCUPATIONS)
        # 7. Exact copies over every input stay: mostly different patients with one profile (LEAK-18, LEAK-19, notes).
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                *SIGNS.values(),
                *COMORBIDITIES.values(),
                *PLACES.values(),
                "sex",
                "pregnancy",
                "race_colour",
                "occupation_cbo",
            ],
            datetime=["notification_date"],
            ordinal={"schooling": SCHOOLING_LEVELS},
        )
