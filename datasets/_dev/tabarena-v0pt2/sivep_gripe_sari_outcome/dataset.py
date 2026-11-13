"""Curated dataset definition for `sivep_gripe_sari_outcome` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
    drop_columns,
    set_missing,
)

# The yearly files (one per epidemiological year of the first symptoms) that hold the admissions of 2023 to June 2026:
# the frozen files of 2022-2024 (of 2026-03-23) and the live files of 2025-2026 (of 2026-11-09).
FILES = (
    "INFLUD22-23-03-2026.parquet",
    "INFLUD23-23-03-2026.parquet",
    "INFLUD24-23-03-2026.parquet",
    "INFLUD25-09-11-2026.parquet",
    "INFLUD26-09-11-2026.parquet",
)
PREPARED = "sivep_srag_2023_2026.parquet"
# The history starts after the COVID-19 emergency (notes, "History") and ends where follow-up is complete (LEAK-24).
FIRST_ADMISSION = "2023-01-01"
LAST_ADMISSION = "2026-06-30"

# The form's yes/no items (1 yes, 2 no, 9 ignored), renamed to English (data dictionary of 25/05/2023, fields 32-41).
SYMPTOMS = {
    "FEBRE": "fever",
    "TOSSE": "cough",
    "GARGANTA": "sore_throat",
    "DISPNEIA": "dyspnoea",
    "DESC_RESP": "respiratory_distress",
    "SATURACAO": "o2_saturation_below_95",
    "DIARREIA": "diarrhoea",
    "VOMITO": "vomiting",
    "DOR_ABD": "abdominal_pain",
    "FADIGA": "fatigue",
    "PERD_OLFT": "loss_of_smell",
    "PERD_PALA": "loss_of_taste",
    "OUTRO_SIN": "other_symptoms",
}
RISK_FACTORS = {
    "PUERPERA": "puerperal",
    "CARDIOPATI": "chronic_cardiovascular_disease",
    "HEMATOLOGI": "chronic_haematological_disease",
    "SIND_DOWN": "down_syndrome",
    "HEPATICA": "chronic_liver_disease",
    "ASMA": "asthma",
    "DIABETES": "diabetes",
    "NEUROLOGIC": "chronic_neurological_disease",
    "PNEUMOPATI": "other_chronic_lung_disease",
    "IMUNODEPRE": "immunodeficiency",
    "RENAL": "chronic_kidney_disease",
    "OBESIDADE": "obesity",
    "OUT_MORBI": "other_risk_factors",
}
OTHER_YES_NO = {
    "NOSOCOMIAL": "hospital_acquired",
    "VACINA": "flu_vaccine_last_campaign",
    "MAE_VAC": "mother_flu_vaccinated",
    "M_AMAMENTA": "breastfed",
    "VACINA_COV": "covid_vaccine",
    "TEM_CPF": "has_cpf",
    "ESTRANG": "foreigner",
    "POV_CT": "traditional_community",
}
PERSON = {
    "CS_SEXO": "sex",
    "CS_GESTANT": "pregnancy",
    "CS_RACA": "race_colour",
    "CS_ETINIA": "indigenous_ethnicity",
    "CS_ESCOL_N": "schooling",
    "TP_POV_CT": "traditional_community_type",
    "CS_ZONA": "residence_zone",
    "AVE_SUINO": "animal_contact",
    "OBES_IMC": "bmi",
}
PLACES = {
    "SG_UF_NOT": "notification_state",
    "ID_REGIONA": "notification_health_region",
    "SG_UF": "residence_state",
    "ID_RG_RESI": "residence_health_region",
    "ID_PAIS": "residence_country",
    "SG_UF_INTE": "hospital_state",
    "ID_RG_INTE": "hospital_health_region",
    "NM_UN_INTE": "hospital",
}
# Municipalities ship as "name [IBGE code]": the names repeat across states.
MUNICIPALITIES = {
    "notification_municipality": ("ID_MUNICIP", "CO_MUN_NOT"),
    "residence_municipality": ("ID_MN_RESI", "CO_MUN_RES"),
    "hospital_municipality": ("ID_MN_INTE", "CO_MU_INTE"),
}
TEXT = {"OUTRO_DES": "other_symptoms_text", "MORB_DESC": "other_risk_factors_text", "OUT_ANIM": "other_animal_text"}
COVID_DOSES = ("DOSE_1_COV", "DOSE_2_COV", "DOSE_REF", "DOSE_2REF", "DOSE_ADIC", "DOS_RE_BI")
# The first COVID-19 vaccination in Brazil; an earlier dose date is a typing error.
FIRST_COVID_DOSE = "2021-01-17"
# Free-text cells that name intensive care, intubation, ventilation, a cardiac arrest or a death: events of the stay
# or the outcome that the dropped fields hold (LEAK-10, LEAK-2). A cell that says the patient arrived so ("chegou em
# IOT") is known at admission and stays; a patient admitted dead has no prediction point.
IN_STAY = (
    r"\bIOT\b|INTUB|\bUTI\b|\bUTIP\b|\bTOT\b|\bVM\b|VENTILA[CÇ]|\bCTI\b|\bPCR\b|PARADA"
    r"|MORTE ENCEF|MORTE CEREBRAL|P[OÓ]S\s*-?\s*[OÓ]BITO|^[OÓ]BITO"
)
ARRIVAL = r"CHEG(?:A|OU)\b|ADMITID\w*\s*(?:EM|COM)\b|RECEBID\w*\s*EM\b"
OUTCOME_WORDS = r"MORTE|[OÓ]BITO|EVOLU|NECESSI|PIORA|DESDE|\bPCR\b|PARADA"
DEAD_ON_ARRIVAL = r"ADMITID\w*\s*(?:EM\s*)?[OÓ]BITO|[OÓ]BITO TRAZIDO"

SCHOOLING_LEVELS = [
    "no schooling",
    "primary 1st cycle (grades 1-5)",
    "primary 2nd cycle (grades 6-9)",
    "secondary",
    "higher education",
]
YES_NO = {"1": "Yes", "2": "No"}
CODE_LABELS = {
    **dict.fromkeys((*SYMPTOMS.values(), *RISK_FACTORS.values(), *OTHER_YES_NO.values()), YES_NO),
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
    "schooling": dict(zip(["0", "1", "2", "3", "4"], SCHOOLING_LEVELS, strict=True)),
    "residence_zone": {"1": "urban", "2": "rural", "3": "periurban"},
    "animal_contact": {"1": "birds or pigs", "2": "none", "3": "other animal"},
}
MISSING_CODES = {
    **{c: ["9"] for c in (*SYMPTOMS.values(), *RISK_FACTORS.values(), *OTHER_YES_NO.values())},
    "sex": ["I"],
    "pregnancy": ["0", "9"],  # 0 is no code of the dictionary
    "race_colour": ["9"],
    "schooling": ["5", "9"],  # 5 "not applicable" (under 7 years) is off the scale (CLEAN-14)
    "residence_zone": ["9"],
    "animal_contact": ["9"],
}

# Filled during the stay or by the investigation after admission, or the outcome itself (LEAK-10; dictionary
# fields 42-98).
AFTER_ADMISSION = [
    *["ANTIVIRAL", "TP_ANTIVIR", "OUT_ANTIV", "DT_ANTIVIR"],  # influenza antiviral: started after admission for 29-48%
    *["TRAT_COV", "TIPO_TRAT", "OUT_TRAT", "DT_TRT_COV"],  # COVID-19 antiviral, the same
    *["UTI", "DT_ENTUTI", "DT_SAIDUTI", "SUPORT_VEN"],  # intensive care and ventilation
    *["RAIOX_RES", "RAIOX_OUT", "DT_RAIOX", "TOMO_RES", "TOMO_OUT", "DT_TOMO"],  # chest X-ray and CT
    *["AMOSTRA", "DT_COLETA", "TP_AMOSTRA", "OUT_AMOST"],  # sample (type 3 is post-mortem tissue)
    *["PCR_RESUL", "DT_PCR", "POS_PCRFLU", "TP_FLU_PCR", "PCR_FLUASU", "FLUASU_OUT", "PCR_FLUBLI", "FLUBLI_OUT"],
    *["POS_PCROUT", "PCR_SARS2", "PCR_VSR", "PCR_PARA1", "PCR_PARA2", "PCR_PARA3", "PCR_PARA4", "PCR_ADENO"],
    *["PCR_METAP", "PCR_BOCA", "PCR_RINO", "PCR_OUTRO", "DS_PCR_OUT"],  # RT-PCR
    *["TP_TES_AN", "DT_RES_AN", "RES_AN", "POS_AN_FLU", "TP_FLU_AN", "POS_AN_OUT", "AN_SARS2", "AN_VSR"],
    *["AN_PARA1", "AN_PARA2", "AN_PARA3", "AN_ADENO", "AN_OUTRO", "DS_AN_OUT"],  # antigen tests
    *["TP_AM_SOR", "SOR_OUT", "DT_CO_SOR", "TP_SOR", "OUT_SOR", "DT_RES", "RES_IGG", "RES_IGM", "RES_IGA"],  # serology
    *["SURTO_SG", "CO_DETEC"],  # outbreak chain and co-detection: investigation results
    *["CLASSI_FIN", "CLASSI_OUT", "CRITERIO", "EVOLUCAO", "DT_EVOLUCA", "DT_ENCERRA"],  # classification and outcome
    *["VG_OMS", "VG_OMSOUT", "VG_LIN", "VG_MET", "VG_METOUT", "VG_DTRES", "VG_ENC", "VG_REINF", "VG_CODEST", "REINF"],
]
SYSTEM = [
    "NU_NOTIFIC",  # record number
    "DT_NOTIFIC",  # notification date: after the prediction point (notes)
    "SEM_NOT",  # epidemiological weeks of the notification and of the onset
    "SEM_PRI",
    "DT_SIN_PRI",  # onset date: kept as the days from onset to admission
    "DT_DIGITA",  # typing date
    "DT_NASC",  # birth date: personal data, the age is kept
    *["NU_IDADE_N", "TP_IDADE", "COD_IDADE"],  # coded age: kept as age_years
    *["CO_REGIONA", "CO_RG_RESI", "CO_RG_INTE", "CO_PAIS"],  # codes of the named regions and country
    *["ID_MUNICIP", "CO_MUN_NOT", "ID_MN_RESI", "CO_MUN_RES", "ID_MN_INTE", "CO_MU_INTE"],  # merged into names [code]
    "HOSPITAL",  # hospitalised: "Yes" on every kept row
    "DT_INTERNA",  # admission date: kept as admission_date
    *["DT_UT_DOSE", *COVID_DOSES],  # vaccination dates: kept as doses and days since the last dose
    *["DT_VAC_MAE", "DT_DOSEUNI", "DT_1_DOSE", "DT_2_DOSE"],  # children's influenza doses (1-2% filled)
    *["FAB_COV_1", "FAB_COV_2", "FAB_COVRF", "FAB_COVRF2", "FAB_ADIC", "FAB_RE_BI"],  # vaccine makers
    *["LOTE_1_COV", "LOTE_2_COV", "LOTE_REF", "LOTE_REF2", "LOTE_ADIC", "LOT_RE_BI"],  # vaccine lots
    "FNT_IN_COV",  # source of the vaccine data (typed or from the national register)
    *["PAC_COCBO", "PAC_DSCBO"],  # merged into occupation
    *["HISTO_VGM", "PAIS_VGM", "CO_PS_VGM", "LO_PS_VGM", "DT_VGM", "DT_RT_VGM"],  # travel: constant or empty
    "TABAG",  # smoking: empty in every file
    "FATOR_RISC",  # "has risk factors": 1 or blank, blank exactly when every risk factor is blank
    "source_file",
]


class SivepGripeSariOutcome(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Will a patient admitted to a Brazilian hospital with severe acute respiratory illness die during the "
            "stay, judged from what the notification form records at admission?"
        ),
        use_case=(
            "The hospital team, when a patient with severe acute respiratory illness (SARI) is admitted, estimates "
            "the risk of death to decide on monitoring and beds, and for a ward patient on early referral to "
            "intensive care (a fifth of the patients go to intensive care on the admission day)."
        ),
        row=(
            "One hospitalised SARI case notified to SIVEP-Gripe, the Ministry of Health's national register, admitted "
            "from January 2023 to June 2026, discharged or dead by the download and notified before the outcome: "
            "790,430 admissions, 9.3% deaths."
        ),
        predicted="Whether the patient died in hospital, of the SARI or of another cause, rather than being discharged.",
        known=(
            "Age, sex, pregnancy, race or colour, schooling, residence, the hospital and its place, the days since the "
            "first symptoms, 13 symptoms (low oxygen saturation among them), 13 risk factors, and the influenza and "
            "COVID-19 vaccinations given before admission."
        ),
        split=(
            "Each test window is a later half-year (January 2025 to June 2026), and training stops one month before "
            "it, as for a model refit twice a year once most earlier cases are closed."
        ),
        changes=(
            "We keep the admissions since 2023 with a known outcome, drop the forms notified on or after the outcome, "
            "count both death codes as death, drop every field filled during the stay and the free-text cells that "
            "name one, take the vaccinations as of admission, and bin the days since a vaccine to 30 days."
        ),
        fit="approximate",
        fit_reason=(
            "The inputs are known at admission and the label is the stay's outcome, but the form holds only part of "
            "what the team knows then (symptoms as yes or no, no vital signs or laboratory values); the forms "
            "notified on or after the outcome (14.4%, a quarter of the deaths) leave, and with them most deaths "
            "on the admission day, so the task covers patients notified during the stay (notes)."
        ),
    )

    # Dataset
    unique_name = "sivep_gripe_sari_outcome"
    year = "2026"
    domain = "medical & healthcare"
    source = "GOV Website"
    source_url = "https://dadosabertos.saude.gov.br/dataset/srag-2019-a-2026"
    license = (
        "CC BY (the dataset page: Creative Commons Atribuição, version not stated; the portal footer: CC BY-ND 3.0)"
    )
    data_tags = ("Spatial",)
    download_description = """
        We download the yearly Parquet files of 2022-2026 and the data dictionary from the Ministry of Health's open-data portal (Portal de Dados Abertos do SUS, dataset "Banco de dados da Síndrome Respiratória Aguda Grave (SRAG) - 2019 a 2026"). The files of 2019-2024 are frozen (of 2026-03-23); the files of 2025 and 2026 are replaced weekly, under a new name, so a later download differs. Ours are of 2026-11-09, with these SHA-256 sums (first 12 hex digits): INFLUD22 93aab4d4ef3a, INFLUD23 3adfca92884f, INFLUD24 015135a33779, INFLUD25 53b4a76e44ae, INFLUD26 51c5fa4c07b5.

        mkdir -p local-data-warehouse/sivep_gripe_sari_outcome && cd local-data-warehouse/sivep_gripe_sari_outcome
        B=https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SRAG
        for y in 22 23 24; do wget $B/20$y/INFLUD$y-23-03-2026.parquet; done
        for y in 25 26; do wget $B/20$y/INFLUD$y-09-11-2026.parquet; done
        wget $B/dicionario-de-dados-2019-a-2025.pdf $B/ficha-de-notificacao-2025.pdf
    """
    bibtex = """
        @misc{ministeriodasaude2026srag,
          author = {{Minist{\\'e}rio da Sa{\\'u}de}},
          title = {Banco de dados da S{\\'i}ndrome Respirat{\\'o}ria Aguda Grave ({SRAG}) - 2019 a 2026},
          howpublished = {Portal de Dados Abertos do SUS, \\url{https://dadosabertos.saude.gov.br/dataset/srag-2019-a-2026}},
          year = {2026},
          note = {SIVEP-Gripe, Sistema de Informa{\\c{c}}{\\~a}o da Vigil{\\^a}ncia Epidemiol{\\'o}gica da Gripe. Files of 2026-11-09},
        }
    """
    curation_comments = """
        We start with the yearly Parquet files INFLUD22 to INFLUD26 of the Ministry of Health's SRAG dataset (SIVEP-Gripe) on the Portal de Dados Abertos do SUS, with its data dictionary of 25/05/2023.

        - Prediction point: the hospital admission of a patient with SARI (the admission date), before anything the stay brings. Only what the form's identification, residence, clinical and vaccination sections hold is a feature: who the patient is, where they live, which hospital admits them, the symptoms and risk factors they present with, and the vaccines they had. Two groups are named: 20.8% of the patients (38% of the deaths) enter intensive care on the admission day, for whom the referral is already made and the score serves monitoring and beds; and 21,213 (2.7%) have a hospital-acquired SARI (7,707 of them with onset after admission), whose moment is the recognition of the SARI, not the admission (USE-3, USE-8).
        - Use case: the hospital team decides at admission how closely to monitor the patient, whether to refer early to intensive care, and plans its beds. Baqui et al. 2021 (Scientific Reports 11:15591) model death against recovery on SIVEP-Gripe for "hospital management and healthcare network organization" and group risk; the per-patient framing is ours. The portal and the data dictionary describe the register, not a prediction.
        - History: we keep the admissions from January 2023 (SPLIT-20). SIVEP-Gripe changed with COVID-19: the portal's notes describe surveillance aimed mainly at influenza before it and widened to other respiratory viruses from 2020 (48,941 notifications in 2019, 1.2M to 1.7M a year in 2020-2021, 0.27M to 0.34M a year since 2023); from April 2020 to September 2021, 61% to 83% of a quarter's cases were COVID-19 and 25% to 34% died; the clinical closing criteria for COVID-19 were dropped on 2022-10-31 (dictionary, field 81); 2022 is a transition (33% to 55% COVID-19, 17% to 27% deaths). Among the admissions since 2023, COVID-19 is 1% to 29% of a quarter's cases and 7% to 15% die. A model refit today would not learn the risk of a SARI patient from the pandemic years, which would also fill most of its training rows (3.5M of the 4.6M notifications since 2020). We download only the files that hold admissions from 2023 on (INFLUD22 to INFLUD26: a case is filed by the year of its first symptoms, so 2,713 admissions of January 2023 are in INFLUD22).
        - Cohort: the notifications marked hospitalised (`HOSPITAL` = 1) with an admission date from 2023-01-01 to 2026-06-30 (987,345). Rows not hospitalised (19,781), with hospitalisation unknown or blank (25,421) or without an admission date (13,670) are no task rows (USE-7). Of the hospitalised, 46,012 (4.7%) were still open at the download and 18,165 (1.8%) closed with outcome "ignored"; they carry no label and leave. Both shares are stable over 2023-2025 (open 2% to 7%, ignored 1% to 2.5% by quarter of notification).
        - End of the data (LEAK-24): the newest admissions are not all closed. For the admissions of January to June 2025, the share closed within a given time of admission is the same for deaths and discharges from 90 days on (94% at 90 days, 97% at 150, 99% at 240), so an admission of June 2026, 132 days before the download, is closed about as often whatever its outcome: we stop at 2026-06-30. Later months are still filling (open 8% in July, 17% in September, 38% in October 2026). The rows still open are riskier: counting them at a model's predicted risk moves the death rate of January-June 2026 from 8.30% to about 8.6%, and a simulated earlier download moves the scored label by 0.05 points; the open share of 2026 rises month by month (4.2% in January to 7.7% in June).
        - Target: `died_in_hospital` is "Yes" for the outcomes death (`EVOLUCAO` = 2, 71,037) and death from other causes (3, 27,150), "No" for cure (1, 824,981; counts of the cohort before the late forms and the copies below are dropped): 10.6% "Yes", 8.3% to 12.7% by half-year. The team acts on the risk of dying in hospital whatever the certified cause, which is set after the death (USE-5); the code-3 deaths are 28% of the deaths. After the drops: 73,555 deaths in 790,430 rows, 9.3%.
        - Forms notified on or after the outcome (LEAK-10, LEAK-6): 132,512 rows (14.4%; 7.5% notified after the patient left, 6.8% on the day of the outcome) hold 25% of the deaths, and leave. In these forms the answers and the blanks follow the outcome: respiratory distress has an odds ratio for death of 3.69 in them against 2.30 in routine forms at the same length of stay, and race is blank for 25.2% of their discharges against 9.7% of their deaths. Kept, they lift the test score by about 0.005 (LightGBM, mean of the three windows: 0.8829 on all test rows against 0.8782 on the routine rows; 0.91-0.92 on the late rows). After the drop the score on the kept rows equals that on the routine rows (0.8782 against 0.8780), and the ranking of LightGBM, random forest and linear models stays. The drop reads the outcome date, which is blank for 6.5% of the kept rows (7.2% of the discharges, 0.5% of the deaths): these undated rows are recognisable from the features (ROC AUC 0.89-0.92) but carry no reverse marker and do not lift the score. The drop changes the population: 97.8% of the deaths on the admission day leave, so the task covers patients notified while in hospital. The curator may keep the rows only through an amendment of LEAK-10 (REVIEW.md, issue 1).
        - Dropped as filled during the stay or by the investigation (LEAK-10; dictionary fields 42-98): the influenza and COVID-19 antivirals (started after the admission day for 29% of the discharged and 42% of the dead who got one), intensive care and its dates, ventilation, chest X-ray and CT, every sample and test (RT-PCR, antigen, serology; sample type 3 is post-mortem tissue), the outbreak and co-detection fields, the final classification and its criterion, the outcome and its date, the closing date and the genomic-surveillance fields.
        - Dropped as system or derived fields: the record number, the notification date and its epidemiological week (the notification comes after the admission: median one day, 90th percentile five), the onset week, the typing date, the coded age (kept as `age_years`), the birth date (personal data), the codes of the named regions and country, the hospitalisation flag (1 on every kept row), the vaccine makers and lot numbers, the source of the vaccine data, the children's influenza dose dates (1% to 2% filled), the travel fields (constant or empty), smoking (empty in every file) and "has risk factors" (1 or blank, blank exactly when every risk factor is blank).
        - Vaccinations (LEAK-10, a value read at a later pull): the COVID-19 doses come mostly from the national vaccination register (96% of the rows), read when the form is completed, so a dose given after discharge appears for survivors only. We keep `covid_vaccine_doses` (the doses dated on or before admission; 0 for "not vaccinated" without dates) and `days_since_covid_vaccine`, and set `covid_vaccine` to "No" where every dated dose is after admission (the state at admission; a blank there marked survivors: 914 of 922 such rows were cures). Dose dates before 2021-01-17, the first vaccination in Brazil, are typing errors and missing. An influenza dose dated after admission (5,519 discharges, 0.67%, against 77 deaths, 0.11%) sets `flu_vaccine_last_campaign` to "No" and is no `days_since_flu_vaccine`. Both day counts ship in 30-day bins (0, 30, 60, ...): the open data has no patient id, but exact vaccination dates single out a person, and a later readmission of that person would tell a model the earlier stay ended alive (LEAK-17; +0.0015 ROC AUC to a participant before the bins, nil after).
        - Built: `age_years` from the coded age (unit days, months or years; negative or over 120 missing), `days_onset_to_admission` (negative for a hospital-acquired SARI; beyond a year either way missing), the vaccination counts above. The admission date stays as a datetime and the task's time column.
        - Codes decoded into the dictionary's words (CLEAN-12): the 13 symptoms and 13 risk factors and the other yes/no items (9 "ignorado" missing), sex (I missing), pregnancy (0, no code, and 9 missing), race or colour (9 missing), residence zone, animal contact, and schooling as an ordered category from no schooling to higher education (9 and blank missing; 5 "not applicable" missing as a state off the scale, CLEAN-14; missing for every patient under 7, whom the dictionary sets to "not applicable", field 19). States stay their abbreviations and health regions their names; municipalities ship as "name [IBGE code]", since names repeat across states, with one name per code (the newest spelling; a few codes had two), and the occupation as "title [CBO code]" from the form's own pair (XXX, not informed, missing; 0.5% filled). The hospital ships as "name [IBGE code of its municipality]" (4,536 levels; 125 names stood for hospitals in several municipalities, and the open data has no CNES code), blank for 3.8%. "Puerperal" is missing for men and children under 10 (the field is for women).
        - Note: a risk factor is blank on 65% to 70% of the rows: the form exports "has risk factors" as 1 or blank, and every factor is blank exactly when it is, so a blank factor mostly means "none reported". Kept as published.
        - Free texts (LEAK-10, LEAK-2): the texts of other symptoms (27% filled), other risk factors (17%) and the other animal (0.3%) stay as text; "?" is missing. A symptom or risk-factor cell that names intensive care, intubation, ventilation, a cardiac arrest or a death is blanked (634 rows of the shipped data, 39% of them deaths), since the dropped intensive-care and ventilation fields came back through them, some from this stay ("evoluiu para IOT", "protocolo de morte encefálica"); a cell that says the patient arrived so ("chegou em IOT") is known at admission and stays (21 rows). Three patients admitted dead ("admitido em óbito") have no prediction point; all three were late forms. The texts in all add about 0.002 ROC AUC.
        - Notified twice (LEAK-18, LEAK-19): 241 rows are equal to another on every column, the admission date, the hospital and the free texts included, and one copy stays. Most are one case notified twice, but 28% of the copy groups hold two birth dates (counted before the drop of the late forms): different infants with one coarse profile, the same day and hospital, so one of two patients is dropped there (LEAK-18, LEAK-19). One pair differs only in the outcome and is dropped (LEAK-20).
        - Exact copies over every input kept as natural repeats (LEAK-18): 0.4% of the test rows (0.2% to 0.5% per window) match a training row on every input but the admission date and the free texts, nearly all with the same label; none with them (leak probe 5). The inputs are mostly yes/no items, so different patients share a profile; the open data has no patient id to find one patient admitted twice (the vaccine dates could rebuild one: binned, see above).
        - Note: age alone scores ROC AUC 0.812 against 0.870 for all features, and 0.848 without it (leak probes before the drop of the late forms, LightGBM on 200,000 rows of each split): the natural core of the task (TP-4). The hospital alone scores 0.727 (0.867 without it): its case mix and care, known at admission (LEAK-34); the hospitals of 94% of the test rows admitted patients in training. Missing vaccination data and blank risk factors carry signal (0.66 to 0.70 alone): no dose before admission, no reported risk factor. The free texts add 0.002 (0.872 with them as text).
        - Note: units that notify mostly deaths (LEAK-25, LEAK-34). Before the drop, 74 hospitals with 30 or more rows had 50% or more deaths (1.6% of the rows, 10.1% of the deaths), mostly emergency units without intensive care whose forms were written after the death (UPA José Santos Sasso and UPA Vicente Missiano in Osasco, PS Municipal Santana in São Paulo); there the hospital records where the patient died rather than the case mix at admission. After the drop, 29 such hospitals remain (0.9% of the rows, 6.3% of the deaths).
        - Note on the metric (MET-8, MET-11): the pooled ROC AUC mixes children (61% of the test rows, 10% of the deaths) and adults; among adults alone the score is about 0.76 against 0.88 pooled, and age alone scores 0.81. ROC AUC does not see calibration: models over-predict the deaths of the test windows by about 12% pooled (a drift of the death rate, 14% in July-December 2025, about 1% in the other windows).
        - Potential leak, kept on purpose: counts of admissions per hospital or state over windows that reach into later days of the test window (feature rows of the test half-year, no label) add about 0.0008 ROC AUC over a strong model with past-only counts, which are legitimate. A participant scores a whole half-year at once, so this transductive use cannot be closed without shorter test blocks, which the refit cadence does not ask for (LEAK-30).
        - Licence: the dataset page names Creative Commons Atribuição (CC BY, version not stated); the portal's footer says CC BY-ND 3.0. Under the footer's reading (no derivatives) a curated table would be a derivative; we take the dataset page's licence, the one stated for this dataset (EV-4, PROV-10).
    """

    # Task
    target = "died_in_hospital"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Baqui et al. 2021 (Scientific Reports 11:15591), the study the use case follows, compare models by ROC AUC "
            "and average precision, and report the sensitivity at a fixed specificity: no single criterion (MET-5). "
            "The portal and the data dictionary define no metric. Fallback ROC AUC on the "
            "probabilities (MET-8): the team ranks the admitted patients by risk."
        )
    )

    # Splits
    splits_comment = """
        A model built on past admissions scores the next patients, refit twice a year. Test windows are the last three half-years with complete follow-up (January-June 2026, July-December 2025, January-June 2025; 120,658, 113,955 and 143,066 rows, 7.6%, 8.4% and 9.0% deaths), newest first; each train side is every admission from January 2023 up to one month before its window (400,458 to 656,906 rows, 51% to 83%). Three windows of six months follow the refit cadence and keep the oldest train side above half the rows (SPLIT-14); the January-June windows hold the influenza and RSV season (18% to 45% more admissions than the second half of 2023-2025).
        Gap: a case is closed a median 11 days after its notification (90% within 55 days). With one month, 0.9% to 1.9% of each train side was still open at its window's start, alike for deaths and discharges (0.9% against 1.0% for the newest window); without it, half of the last month's rows were open at the start, more of the deaths (53% to 62% against 47% to 51%). A participant must not train on the rows of the gap month.
        History: from January 2023, after the COVID-19 years (notes). COVID-19 is 18% to 22% of the admissions of January-February 2025 and under 9% from March 2025 on, against 3% to 29% a quarter in 2023-2024 (above 25% in January-March 2023, October 2023-March 2024), so the newest windows hold less of it than the history.
    """
    temporal = Temporal(
        on="admission_date",
        splits=TemporalSplits(window=6, unit="months", cutoffs=("2025-01-01", "2025-07-01", "2026-01-01"), gap=1),
    )

    prepared_raw_files = (PREPARED,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # The five yearly files (1.4M notifications, 194 columns) are read whole, every column cast to text except the
        # dates, and only the notifications made or admitted from 2023 on are kept, every column as published.
        import pyarrow as pa
        import pyarrow.compute as pc
        import pyarrow.parquet as pq

        start = pa.scalar(pd.Timestamp(FIRST_ADMISSION), pa.timestamp("ns"))
        tables = []
        for name in FILES:
            table = pq.read_table(raw_dir / name)
            schema = pa.schema(
                [f if pa.types.is_timestamp(f.type) else pa.field(f.name, pa.string()) for f in table.schema]
            )
            table = table.cast(schema)
            keep = pc.or_kleene(
                pc.greater_equal(table.column("DT_NOTIFIC"), start), pc.greater_equal(table.column("DT_INTERNA"), start)
            )
            table = table.filter(pc.fill_null(keep, False))
            tables.append(table.append_column("source_file", pa.array([name[:8]] * table.num_rows, pa.string())))
        pq.write_table(pa.concat_tables(tables), raw_dir / PREPARED)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        import pyarrow.parquet as pq

        return pq.read_table(raw_dir / PREPARED).to_pandas()

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        # 1. The cohort: hospitalised cases admitted from 2023 to June 2026 with a known outcome (cure, death, death
        #    from another cause); the open and "ignored" outcomes carry no label.
        df["admission_date"] = df["DT_INTERNA"]
        df = df[(df["HOSPITAL"] == "1") & df["admission_date"].between(FIRST_ADMISSION, LAST_ADMISSION)]
        df = df[df["EVOLUCAO"].isin(["1", "2", "3"])]
        # Forms notified on or after the outcome date describe the admission as known once the stay was over: their
        # answers and blanks follow the outcome (LEAK-10, LEAK-6; notes).
        df = df[~(df["DT_NOTIFIC"] >= df["DT_EVOLUCA"])]
        # A patient admitted dead has no prediction point (LEAK-36, USE-7).
        texts = (df["OUTRO_DES"].fillna("") + " || " + df["MORB_DESC"].fillna("")).str.upper()
        df = df[~texts.str.contains(DEAD_ON_ARRIVAL, regex=True)]
        # A record in a frozen file and again in the next year's live file (17 records, its onset re-dated) is one
        # case: the newer copy stays (the files are in FILES order).
        df = df.drop_duplicates("NU_NOTIFIC", keep="last")
        df[self.target] = np.where(df["EVOLUCAO"] == "1", "No", "Yes")
        # 2. Age in years from the coded age (unit 1 days, 2 months, 3 years); over 120 is a recording error.
        age = pd.to_numeric(df["NU_IDADE_N"], errors="coerce")
        scale = df["TP_IDADE"].map({"1": 1 / 365.25, "2": 1 / 12, "3": 1.0})
        df["age_years"] = (age * scale).where(lambda a: a.between(0, 120))
        # 3. Days from the first symptoms to admission: negative for a hospital-acquired SARI; over a year either way
        #    is a mistyped year.
        lag = (df["admission_date"] - df["DT_SIN_PRI"]).dt.days
        df["days_onset_to_admission"] = lag.where(lag.between(-365, 365))
        # 4. Vaccinations given before admission (LEAK-10: the national register is read after the stay, so a dose
        #    given after discharge appears for survivors only).
        doses = pd.concat([pd.to_datetime(df[c], format="%d/%m/%Y", errors="coerce") for c in COVID_DOSES], axis=1)
        doses = doses.where(doses >= pd.Timestamp(FIRST_COVID_DOSE))
        before = doses.where(doses.le(df["admission_date"], axis=0))
        dated = doses.notna().any(axis=1)
        df["covid_vaccine_doses"] = before.notna().sum(axis=1).where(dated | (df["VACINA_COV"] == "2"))
        # Day counts in 30-day bins: exact vaccination dates single out a person across admissions (LEAK-17).
        df["days_since_covid_vaccine"] = (df["admission_date"] - before.max(axis=1)).dt.days // 30 * 30
        # No dose dated before admission: "not vaccinated" as of admission, whatever the form says later.
        all_after = dated & before.isna().all(axis=1)
        df.loc[all_after, "VACINA_COV"] = "2"
        flu_after = df["DT_UT_DOSE"] > df["admission_date"]
        df.loc[flu_after & (df["VACINA"] == "1"), "VACINA"] = "2"
        df["days_since_flu_vaccine"] = (df["admission_date"] - df["DT_UT_DOSE"].where(~flu_after)).dt.days // 30 * 30
        # 5. Municipalities as "name [IBGE code]", one name per code (its newest spelling); the hospital as "name
        #    [IBGE code of its municipality]", since hospital names repeat across municipalities; the occupation as "title [CBO code]" from the form's own pair
        #    ("XXX", not informed, is missing).
        newest = df.sort_values("admission_date", kind="stable")
        for new, (name, code) in MUNICIPALITIES.items():
            spelling = newest.dropna(subset=[name, code]).drop_duplicates(code, keep="last").set_index(code)[name]
            df[new] = (df[code].map(spelling) + " [" + df[code] + "]").where(df[code].notna())
        hospital_code = (" [" + df["CO_MU_INTE"] + "]").fillna("")
        df["NM_UN_INTE"] = (df["NM_UN_INTE"] + hospital_code).where(df["NM_UN_INTE"].notna())
        known = df["PAC_COCBO"].notna() & (df["PAC_COCBO"] != "XXX")
        df["occupation"] = (df["PAC_DSCBO"] + " [" + df["PAC_COCBO"] + "]").where(known)
        # 6. BMI typed as text; values outside 10-100 are recording errors.
        bmi = pd.to_numeric(df["OBES_IMC"], errors="coerce")
        df["OBES_IMC"] = bmi.where(bmi.between(10, 100))
        # 7. Drop what the stay and the investigation fill, and the system fields; rename, then decode the codes.
        df = drop_columns(df, [*AFTER_ADMISSION, *SYSTEM])
        df = df.rename(columns={**SYMPTOMS, **RISK_FACTORS, **OTHER_YES_NO, **PERSON, **PLACES, **TEXT})
        df = set_missing(df, MISSING_CODES)
        df = decode(df, CODE_LABELS)
        # Impossible values (CLEAN-11): "puerperal" for men and children under 10; schooling under 7 years, which the
        # dictionary sets to "not applicable" (field 19).
        df.loc[(df["sex"] == "male") | (df["age_years"] < 10), "puerperal"] = None
        df.loc[df["age_years"] < 7, "schooling"] = None
        # 8. Free text: a lone "?" is missing; a cell that names an event of the stay or the outcome is blanked.
        for col in TEXT.values():
            df[col] = df[col].mask(df[col].str.strip().isin(["?", "??"]))
        for col in ("other_symptoms_text", "other_risk_factors_text"):
            text = df[col].str.upper()
            arrival = text.str.contains(ARRIVAL, regex=True) & ~text.str.contains(OUTCOME_WORDS, regex=True)
            df[col] = df[col].mask(text.str.contains(IN_STAY, regex=True) & ~arrival.fillna(False))
        # 9. Rows equal on every column, the admission date, the hospital and the free texts included, are one case
        #    notified twice (LEAK-18, LEAK-19): one copy stays. A pair that differs only in the outcome is dropped
        #    whole (LEAK-20).
        df = df.drop_duplicates()
        df = df[~df.drop(columns=self.target).duplicated(keep=False)]
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                *SYMPTOMS.values(),
                *RISK_FACTORS.values(),
                *OTHER_YES_NO.values(),
                *PLACES.values(),
                *MUNICIPALITIES,
                "sex",
                "pregnancy",
                "race_colour",
                "indigenous_ethnicity",
                "traditional_community_type",
                "residence_zone",
                "animal_contact",
                "occupation",
            ],
            string=list(TEXT.values()),
            datetime=["admission_date"],
            ordinal={"schooling": SCHOOLING_LEVELS},
        )
