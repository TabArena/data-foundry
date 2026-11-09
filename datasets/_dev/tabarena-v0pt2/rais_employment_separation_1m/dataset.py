"""Curated dataset definition for `rais_employment_separation_1m` (data-foundry v2). Evidence: README.md."""

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
    decode,
    drop_columns,
    set_missing,
)

YEAR = 2025
"""The base year we ship: the newest RAIS release (PDET FTP, files of 2026-05-13)."""

EXTRACTED = f"extracted/{YEAR}"
"""The seven regional link files of the year (``RAIS_VINC_PUB_<region>.COMT``), unpacked from their .7z archives."""

PREPARED = f"links_{YEAR}_feb1_cohort_sample.parquet"
PREPARED_COUNTS = f"links_{YEAR}_feb1_cohort_counts.csv"

SAMPLE_ROWS = 2_000_000
"""Links drawn from the cohort (uniformly, seed 42) before the row budget's stratified 1.5M (version_comment)."""

SAMPLE_SEED = 42

HEADER = (
    "Bairros SP - Código", "Bairros Fortaleza - Código", "Bairros RJ - Código", "Causa Afastamento 1 - Código",
    "Causa Afastamento 2 - Código", "Causa Afastamento 3 - Código", "Motivo Desligamento - Código",
    "CBO 2002 Ocupação - Código", "CNAE 2.0 Classe - Código", "CNAE 95 Classe - Código", "Distritos SP - Código",
    "Ind Vínculo Ativo 31/12 - Código", "Faixa Etária - Código", "Faixa Rem Média (SM) - Código",
    "Faixa Hora Contrat - Código", "Faixa Rem Dez (SM) - Código", "Faixa Tempo Emprego - Código",
    "Escolaridade Após 2005 - Código", "Qtd Hora Contr", "Idade", "Ind CEI Vinculado - Código",
    "Ind Estabelecimento Participante SIMPLES - Código", "Mês Admissão - Código", "Mês Desligamento - Código",
    "Município Trab - Código", "Município - Código", "Nacionalidade - Código", "Natureza Jurídica - Código",
    "Ind Portador Defic - Código", "Qtd Dias Afastamento", "Raça Cor - Código", "Região Adm DF - Código",
    "Vl Rem Dezembro Nom", "Vl Rem Dezembro (SM)", "Vl Rem Média Nom", "Vl Rem Média (SM)",
    "CNAE 2.0 Subclasse - Codigo", "Sexo - Código", "Tamanho Estabelecimento - Código", "Tempo Emprego",
    "Tipo Admissão Trabalhador - Código", "Tipo Estabelecimento - Código", "Tipo Estabelecimento - Nome",
    "Tipo Deficiência - Código", "Tipo Vínculo - Código", "IBGE Subsetor - Código", "Vl Rem Janeiro SC",
    "Vl Rem Fevereiro SC", "Vl Rem Março SC", "Vl Rem Abril SC", "Vl Rem Maio SC", "Vl Rem Junho SC",
    "Vl Rem Julho SC", "Vl Rem Agosto SC", "Vl Rem Setembro SC", "Vl Rem Outubro SC", "Vl Rem Novembro SC",
    "Ano Chegada Brasil", "Ind Trabalho Intermitente - Código", "Ind Trabalho Parcial - Código",
    "Ind Vínculo Abandonado - Código", "Categoria Trabalhador - Código",
)  # fmt: skip
"""The 62 columns of the 2023-2025 link files (Latin-1 header, comma-separated)."""

READ_INTEGER = {
    # the target's source and the cohort
    "Motivo Desligamento - Código": "separation_reason",
    "Mês Admissão - Código": "admission_month",
    "Mês Desligamento - Código": "separation_month",
    "Ind Vínculo Ativo 31/12 - Código": "active_dec31",
    # the worker
    "Sexo - Código": "sex",
    "Raça Cor - Código": "race",
    "Idade": "age",
    "Escolaridade Após 2005 - Código": "education",
    "Nacionalidade - Código": "nationality",
    "Ind Portador Defic - Código": "disability",
    "Tipo Deficiência - Código": "disability_type",
    # the job
    "CBO 2002 Ocupação - Código": "occupation_cbo",
    "Tipo Vínculo - Código": "contract_type",
    "Categoria Trabalhador - Código": "worker_category",
    "Tipo Admissão Trabalhador - Código": "admission_type",
    "Qtd Hora Contr": "weekly_hours",
    "Ind Trabalho Parcial - Código": "part_time",
    "Ind Trabalho Intermitente - Código": "intermittent",
    # the establishment
    "CNAE 2.0 Subclasse - Codigo": "cnae_subclass",
    "CNAE 2.0 Classe - Código": "cnae_class",
    "IBGE Subsetor - Código": "ibge_subsector",
    "Natureza Jurídica - Código": "legal_nature",
    "Tipo Estabelecimento - Código": "establishment_type",
    "Ind Estabelecimento Participante SIMPLES - Código": "simples",
    "Ind CEI Vinculado - Código": "cei_linked",
    "Município - Código": "municipality",
    "Município Trab - Código": "work_municipality",
    "Bairros SP - Código": "neighbourhood_sao_paulo",
    "Bairros Fortaleza - Código": "neighbourhood_fortaleza",
    "Bairros RJ - Código": "neighbourhood_rio",
    "Distritos SP - Código": "district_sao_paulo",
    "Região Adm DF - Código": "region_federal_district",
    # read for the decisions only, dropped in `_clean` (recorded after the prediction point)
    "Tamanho Estabelecimento - Código": "establishment_size_dec31",
    "Qtd Dias Afastamento": "leave_days",
    "Ind Vínculo Abandonado - Código": "abandoned",
}
"""The columns we read as integer codes or counts, with our names."""

READ_DECIMAL = {
    "Tempo Emprego": "tenure_end",  # months, to 31/12 or to the separation
    "Vl Rem Janeiro SC": "pay_january",  # nominal R$
    "Vl Rem Dezembro Nom": "pay_december",  # for the decisions only
}

# Not read (curation_comments, "Not read"): the leave causes (recorded through the year), the pay of February to
# November and the year's average and December pay with their bands (after the prediction point), the bands of age,
# hours and tenure (copies of `age`, `weekly_hours` and the year-end tenure), `Tipo Estabelecimento - Nome` (a copy of
# its code), `Ano Chegada Brasil` (one value, 1198, in every row) and the CNAE 95 class (the ministry's conversion of
# the declared CNAE 2.0 code into the 1995 classification).

QUIT_REASONS = (20, 21)
"""Separations at the employee's initiative: 20 "rescisão com justa causa por iniciativa do empregado (rescisão
indireta)", 21 "rescisão sem justa causa por iniciativa do empregado ou exoneração a pedido" (RAIS layout 2020)."""

SEPARATION_REASONS = {
    0: "not separated in the year",
    10: "dismissal with just cause",
    11: "dismissal without just cause",
    12: "end of the contract",
    20: "termination with just cause at the employee's initiative (rescisao indireta)",
    21: "termination without just cause at the employee's initiative, or resignation of a servant",
    22: "a servant takes another post that cannot be held with this one",
    30: "transfer, with cost to the sender",
    31: "transfer, without cost to the sender",
    32: "readaptation or redistribution of a servant",
    33: "assignment (cessao)",
    34: "redistribution of a servant",
    40: "change of employment regime",
    50: "military reform to the paid reserve",
    60: "death",
    62: "death from a work accident",
    63: "death from a commuting accident",
    64: "death from an occupational disease",
    70: "retirement for length of service, with termination",
    90: "termination by agreement (art. 484-A CLT)",
}
"""`Motivo Desligamento` (RAIS layout 2020), for the decision table only."""

ESTABLISHMENT_SIZES = {
    1: "Zero", 2: "1 to 4", 3: "5 to 9", 4: "10 to 19", 5: "20 to 49", 6: "50 to 99", 7: "100 to 249",
    8: "250 to 499", 9: "500 to 999", 10: "1000 or more",
}  # fmt: skip
"""`Tamanho Estabelecimento` (RAIS layout 2020: active links on 31/12), for the decision table only."""

EDUCATION_LEVELS = {
    1: "Illiterate",
    2: "Primary, up to 5th year incomplete",
    3: "Primary, 5th year complete",
    4: "Primary, 6th to 9th year",
    5: "Lower secondary complete",
    6: "Upper secondary incomplete",
    7: "Upper secondary complete",
    8: "Higher education incomplete",
    9: "Higher education complete",
    10: "Master's degree",
    11: "Doctorate",
}
"""`Escolaridade Após 2005` (RAIS layout 2020: ANALFABETO, ATE 5.A INC, 5.A CO FUND, 6. A 9. FUND, FUND COMPL, MEDIO
INCOMP, MEDIO COMPL, SUP. INCOMP, SUP. COMP, MESTRADO, DOUTORADO), lowest first."""

CONTRACT_TYPES = {
    10: "CLT, urban, company employer, open-ended",
    15: "CLT, urban, individual employer, open-ended",
    20: "CLT, rural, company employer, open-ended",
    25: "CLT, rural, individual employer, open-ended",
    30: "Statutory civil servant",
    31: "Statutory civil servant, general social security",
    35: "Statutory, not tenured",
    40: "Casual worker (avulso)",
    50: "Temporary worker",
    55: "Apprentice",
    60: "CLT, urban, company employer, fixed term",
    65: "CLT, urban, individual employer, fixed term",
    70: "CLT, rural, company employer, fixed term",
    75: "CLT, rural, individual employer, fixed term",
    80: "Director",
    90: "Fixed-term contract (Law 9,601/1998)",
    95: "Fixed-term contract (CONT TMP DET)",
    96: "Fixed-term contract under a state law",
    97: "Fixed-term contract under a municipal law",
}
"""`Tipo Vínculo` (RAIS layout 2020: CLT U/PJ IND ... CONT LEI MUN). CLT is the labour code's employment contract."""

WORKER_CATEGORIES = {
    101: "Employee, general",
    102: "Employee, short-term rural worker",
    103: "Employee, apprentice",
    105: "Employee, fixed-term contract (Law 9,601/1998)",
    106: "Temporary worker (Law 6,019/1974)",
    107: "Employee, Verde e Amarelo contract without FGTS agreement",
    108: "Employee, Verde e Amarelo contract with FGTS agreement",
    111: "Employee, intermittent contract",
    201: "Casual port worker",
    202: "Casual worker, not port",
    301: "Public servant, tenured post",
    302: "Public servant, commissioned post only",
    305: "Public servant appointed to a council",
    306: "Public servant, fixed-term special regime",
    307: "Military, states and Federal District",
    309: "Public agent, other",
    310: "Public servant, occasional",
    314: "Military, armed forces",
    401: "Union leader",
    410: "Worker on loan to another body",
    721: "Non-employee director with FGTS",
}
"""`Categoria Trabalhador`: the eSocial worker category (eSocial layout S-1.3, Tabela 01)."""

ADMISSION_TYPES = {
    0: "Not admitted in the year",
    1: "First job",
    2: "Re-employment",
    3: "Transfer, with cost to the sender",
    4: "Transfer, without cost to the sender",
    6: "Reinstatement",
}
"""`Tipo Admissão Trabalhador` (RAIS layout 2020); code 5 is undocumented and set to missing."""

ESTABLISHMENT_TYPES = {
    1: "CNPJ (company register)",
    3: "CEI (specific register)",
    5: "CAEPF (individual employer register)",
    6: "CNO (construction works register)",
}
"""`Tipo Estabelecimento`: the codes of the file's own `Tipo Estabelecimento - Nome` column (CNPJ, CAEPF, CNO)."""

IBGE_SUBSECTORS = {
    1: "Mineral extraction",
    2: "Non-metallic mineral products",
    3: "Metallurgy",
    4: "Mechanical industry",
    5: "Electrical and communication equipment",
    6: "Transport equipment",
    7: "Wood and furniture",
    8: "Paper, cardboard, publishing and printing",
    9: "Rubber, tobacco, leather and other industries",
    10: "Chemicals, pharmaceuticals and cosmetics",
    11: "Textiles and clothing",
    12: "Footwear",
    13: "Food, beverages and ethyl alcohol",
    14: "Public utility services",
    15: "Construction",
    16: "Retail trade",
    17: "Wholesale trade",
    18: "Credit, insurance and capitalization",
    19: "Real estate, securities and technical services",
    20: "Transport and communications",
    21: "Lodging, food, repair and maintenance services",
    22: "Medical, dental and veterinary services",
    23: "Education",
    24: "Public administration",
    25: "Agriculture, forestry, livestock and plant extraction",
}
"""`IBGE Subsetor` (RAIS layout 2020); code 98, the links whose CNAE class is 99999, is set to missing."""

FLAG = {0: "No", 1: "Yes"}

CODE_LABELS = {
    "education": EDUCATION_LEVELS,
    "contract_type": CONTRACT_TYPES,
    "worker_category": WORKER_CATEGORIES,
    "admission_type": ADMISSION_TYPES,
    "establishment_type": ESTABLISHMENT_TYPES,
    "ibge_subsector": IBGE_SUBSECTORS,
    "simples": FLAG,
    "part_time": FLAG,
}

CODE_WIDTHS = {
    "occupation_cbo": 6,
    "cnae_subclass": 7,
    "cnae_class": 5,
    "legal_nature": 4,
    "municipality": 6,
    "work_municipality": 6,
}
"""Codes of national classifications kept as codes (curation_comments), as zero-padded text of their width."""

PROXY_MISSING = {
    "weekly_hours": [0, 99],  # the hours band of these rows is 99, {ñ class} (Norte 2025: every row)
    "contract_type": [999],
    "admission_type": [5],
    "ibge_subsector": [98],
    "occupation_cbo": [999999],
    "cnae_subclass": [9999999],
    "cnae_class": [99999],
    "legal_nature": [9999],
}
"""Proxy missing values (CLEAN-10): the layouts' "ignorado" codes; the municipalities' "<UF>9999" and 999999 are set to
missing in `_clean`."""

PROTECTED_GROUNDS = ["sex", "race", "age", "nationality", "disability", "disability_type"]
"""Grounds Lei 9.029/1995 art. 1 bars an employer from using to give or keep a job (curation_comments): dropped."""

ARMED_FORCES = 314
"""eSocial worker category of the armed forces, whose separations the 2025 files do not record (decision 5)."""

SEPARATION_DAY = 0.42
"""The mean part of its month that has passed at a separation, over the 2025 leavers hired in January to April (their
tenure to the separation against the stayers' of the same admission month); the day is not published."""

FIXED_TERM_TO_OPEN_ENDED = {60: 10, 65: 15, 70: 20, 75: 25}
"""The CLT fixed-term contract types and their open-ended twins (`CONTRACT_TYPES`)."""

RECENT_HIRE_MONTHS = 3
"""Up to this tenure on 1 February, a CLT fixed-term type is merged into its open-ended twin (decision 6)."""

AFTER_PREDICTION_POINT = [
    "separation_reason",  # the target's source
    "separation_month",
    "admission_month",  # 0 or 1 in the cohort, encoded in tenure_months
    "active_dec31",  # the separation, again
    "tenure_end",  # tenure to 31/12 or to the separation; replaced by tenure_months
    "pay_december",  # 0 or missing after a separation
    "establishment_size_dec31",  # the establishment's active links on 31/12, this link included
    "leave_days",  # days of leave over the whole year
    "abandoned",  # used to drop the abandoned links (step 1), then 0 in every row
]

SUB_MUNICIPAL = [
    "neighbourhood_sao_paulo",
    "neighbourhood_fortaleza",
    "neighbourhood_rio",
    "district_sao_paulo",
    "region_federal_district",
]
"""Codes that divide four cities: 999997 (outside the city) in every link of 2024 and 2025, the cities' too."""

COPIES = [
    "cei_linked",  # = establishment_type == CNO
    "intermittent",  # = worker_category == "Employee, intermittent contract"
]


class RaisEmploymentSeparation1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will an employee in a formal job in Brazil, in post on 1 February, resign before the year ends?",
        use_case=(
            "In early February, after the January payroll, an employer's HR team scores its staff for the risk that "
            "they resign during the rest of the year, to decide whom to offer retention measures (a raise, a talk, a "
            "training plan) and how much hiring to plan."
        ),
        row=(
            "One formal employment link (a worker's job at one establishment) in post on 1 February 2025, from RAIS, "
            "the annual report of formal jobs every Brazilian employer files: a random 1.5 million of the 58.6 "
            "million such links, all employers and sectors pooled, public servants included."
        ),
        predicted=(
            "Whether the employee ended the job at their own initiative between February and December 2025, by "
            "resigning or for the employer's fault (7.3% did); dismissals, ends of contract, agreements, transfers, "
            "retirements and deaths count as no."
        ),
        known=(
            "The worker's education; the job's occupation, contract type, worker category, weekly hours, part-time "
            "flag, tenure on 1 February and January pay; the establishment's sector, legal form, tax regime, register "
            "type and municipality. Not the worker's sex, race, age, nationality or disability: Brazilian law bars an "
            "employer from using them to keep a job."
        ),
        split=(
            "Random links of 2025 in three folds of 1 million training and 500,000 test links: one year, because the "
            "move to eSocial in 2022 and 2023 broke the series, so the split is not by time (a model trained on 2024 "
            "scores about 0.006 ROC AUC lower)."
        ),
        changes=(
            "We build the cohort, the target and the tenure on 1 February; drop what is recorded later in the year, "
            "the links whose outcome the source does not record (flagged abandoned, and the armed forces) and the "
            "grounds the employer may not use; and show recent hires' fixed-term contracts as open-ended, as the "
            "file keeps the type after a later conversion."
        ),
        fit="approximate",
        fit_reason=(
            "The cohort, prediction point and target are ours; the split is random within one year and the files "
            "hold no worker or workplace history. Employers are pooled, with public servants and military (20% of "
            "links) no private HR team scores: 0.789 ROC AUC pooled, 0.746 on private employees, model order kept. "
            "7.7% are dormant links; some quits are filed as dismissals: label noise."
        ),
    )

    # Dataset
    unique_name = "rais_employment_separation_1m"
    version_of = "rais_employment_separation"
    version_comment = """
        The task is every link in post on 1 February 2025: 58,571,381 links of the year's files, 4,188,474 of whom quit. `_prepare_raw_files` draws 2,000,000 of them uniformly (seed 42), so the frame fits in memory; after the abandoned links (24,481) and the armed forces (14,319) leave, the v2 split protocol sub-samples 1.5M links stratified on the target and uses 3-fold cross-validation, so every fold trains on 1M and tests on 500k links.
    """
    year = "2026"
    domain = "social science"
    source = "GOV Website"
    source_url = "https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/microdados-rais-e-caged"
    license = "CC BY-ND 3.0 (the gov.br site's statement for its content; the FTP microdata state none of their own)"
    data_tags = ("Spatial", "ForcedIIDFromTemporal")
    download_description = """
        The seven regional link files of RAIS base year 2025 from the PDET FTP of the Ministry of Labour and Employment
        (files of 2026-05-13; most browsers no longer open FTP, curl does), unpacked with 7-Zip or py7zr into
        extracted/2025. The definition reads the unpacked .COMT files (comma-separated text, about 23 GB); the
        establishment file (RAIS_ESTAB_PUB.7z) is not used. Base year 2024 (the same seven files under .../RAIS/2024/,
        into raw/2024 and extracted/2024) was downloaded only to measure the cost of the random split
        (curation_comments).

        mkdir -p local-data-warehouse/rais_employment_separation/raw/2025 local-data-warehouse/rais_employment_separation/extracted/2025
        cd local-data-warehouse/rais_employment_separation
        for r in CENTRO_OESTE MG_ES_RJ NI NORDESTE NORTE SP SUL; do
          curl -o raw/2025/RAIS_VINC_PUB_$r.7z ftp://ftp.mtps.gov.br/pdet/microdados/RAIS/2025/RAIS_VINC_PUB_$r.7z
          uvx --from py7zr py7zr x raw/2025/RAIS_VINC_PUB_$r.7z extracted/2025   # or: 7z x -oextracted/2025 ...
        done
        sha256sum raw/2025/*.7z
        # 0e4459ee90c0219d9b40b9d6129e494034b8d6cd4dbe86eeb1f49e54f964d724  RAIS_VINC_PUB_CENTRO_OESTE.7z (354,015,896 bytes)
        # d9c4e359fa16c6a1f929f49c8aec0201a9fbfb801964dc2e27032914924f1f15  RAIS_VINC_PUB_MG_ES_RJ.7z (766,814,132 bytes)
        # dfd32817429cb732963b538d987c1537b12e119e81f667c3f7ffeb279ec0c201  RAIS_VINC_PUB_NI.7z (209,311 bytes)
        # 4366dda32c86e5fdb16f62b09028c7c693852f9b44118cd5536d79613eced089  RAIS_VINC_PUB_NORDESTE.7z (639,823,548 bytes)
        # c7deb880bf43db4e0250c1cba20a84a61dcedc6d1888a0687a18b01483ce2e29  RAIS_VINC_PUB_NORTE.7z (211,992,734 bytes)
        # d19f924d71578c782408678888ee59d89b05688e3b31babc1f174d06270d29df  RAIS_VINC_PUB_SP.7z (1,107,305,918 bytes)
        # c537caaaa8318b04e6f4cbbc7e59b130988668b7ea58ce67a0ab2caebf2f5bd0  RAIS_VINC_PUB_SUL.7z (704,888,712 bytes)

        The codebook is the 2020 layout of the link files (ftp://ftp.mtps.gov.br/pdet/microdados/RAIS/Layouts/vínculos/
        RAIS_vinculos_layout2020.xls); the 2023-2025 files keep its codes under new column names, and the de-para table
        the ministry's notice of 2025-12-30 announces is not on the FTP. The worker category is eSocial's Tabela 01
        (https://www.gov.br/esocial/pt-br/documentacao-tecnica/leiautes-esocial-v-s-1-3-cons-nt-05-2025/tabelas.html).
    """
    bibtex = r"""
        @misc{mte2026rais,
          author = {{Minist{\'e}rio do Trabalho e Emprego}},
          title = {Rela{\c{c}}{\~a}o Anual de Informa{\c{c}}{\~o}es Sociais ({RAIS}): microdados n{\~a}o identificados, v{\'i}nculos, ano-base 2025},
          year = {2026},
          howpublished = {\url{ftp://ftp.mtps.gov.br/pdet/microdados/RAIS/2025/}},
          note = {Programa de Dissemina{\c{c}}{\~a}o das Estat{\'i}sticas do Trabalho (PDET), Microdados RAIS e CAGED, \url{https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/microdados-rais-e-caged}}
        }
    """
    curation_comments = """
        We start with the seven regional link files (RAIS_VINC_PUB_*.7z) of RAIS base year 2025 from the PDET FTP of Brazil's Ministry of Labour and Employment (MTE): 91,710,262 employment links, one row per link and year, with no worker or employer id.

        - Prediction point: 1 February 2025, when an employer's HR team, after the January payroll, scores its staff for the risk of resigning during the rest of the year. The source names no prediction (RAIS is a labour census): the use case, the cohort and the target are ours. February rather than 1 January because January's pay is the first pay the files hold that is known before the outcome; they carry no contracted wage.
        - Cohort: the links admitted before February (`Mês Admissão` 0, before the year, or 1, January) and not separated in January: 58,571,381 links (decision 1); 6.1% of the links we keep were hired in January.
        - Target: `quit_by_year_end` is Yes for a separation at the employee's initiative from February to December, codes 20 (rescisão indireta, the employee ends the contract for the employer's fault) and 21 (resignation, or a servant's exoneração a pedido); 7.15% of the cohort, 7.28% of the links we keep (decision 2). Dismissals, ends of contract, transfers, retirements and deaths after 1 February count as No: a competing event keeps its label (LEAK-22). Six codes of the 2023-2025 files are not in the 2020 layout (24, 35, 36, 65, 81, 82: 3,038 links of the sample, 0.15%) and count as No. By age and category 81 and 82 look like servants' retirements; 24 (58 links, mostly CLT employees, median age 38) could be an employee's initiative. The ministry's de-para table, which would settle them, is not on the FTP.
        - Target, agreements: code 90 (termination by agreement, art. 484-A CLT; 6,488 links of the sample, 4.5% of the Yes count if added) counts as No, a call on what the actor acts on (USE-5) left to the curator. By the features an agreement looks like a dismissal without cause: an untuned model of quits ranks the links ended by agreement above the stayers at ROC AUC 0.66-0.67, dismissals without cause at 0.69, resignations at 0.82 (3 shipped folds); counting them Yes lowers the score by 0.006-0.008 and keeps the order of five learners.
        - Note: some quits are filed as dismissals without cause (code 11), the "fake layoff" agreements by which a worker who wants to leave draws the severance fund (FGTS) and unemployment insurance (Dias de Aquino Nascimento 2026, PUC-Rio master's dissertation, after Gonzaga 2003 and Carvalho, Corbi and Narita 2018). They sit in No and cannot be told apart: label noise that caps every model (USE-8).
        - Dropped the abandoned links (`Ind Vínculo Abandonado`, 24,481 of the sample, 1.2%): none has a separation, and every one has no pay in January and in December, against 15% and 18% of the other links in post on 31 December (decision 4). The source will never record their outcome, so they are rows without a target (LEAK-25, CLEAN-15). The flag is not the whole unrecorded pattern: the armed forces' outcomes are not recorded in 2025 (next bullet).
        - Dropped the armed forces (eSocial worker category 314; 14,319 links of the sample, 0.7%): the 2025 files record 3 separations in their 418,633 links, against 254 of 12,651 links (2.0%) in the 2024 sample built by this code, and 85% of them have no January pay, against 3.3% in 2024. A change in the recording, not in behaviour: their No is not recorded (LEAK-25; decision 5).
        - Kept, with a note: 7.7% of the links we keep were paid in no month of 2025 and had no leave day (measured on the sample with the monthly pay of February to November, which the definition does not read); 0.9% of them quit (7.8% of the others) and 6.0% separate (29.5%). They are mostly long-dormant links, not unrecorded outcomes. Of the Norte links in post on 31 December 2024 that had been paid in no month and had no leave, a year later 4.2% had separated with a reason, 11.1% were paid again and 1.1% carried the abandoned flag (persistent: 98.9% of the 2024 flags recur), and 79% of the 2025 group in Norte had been paid in no month and on no leave all through 2024. The source records their outcomes when they come, so the abandoned-link rule does not reach them (LEAK-25), and a filter on the year's pay would select the cohort on the future (LEAK-22). Left out, the score drops by 0.013 ROC AUC (untuned LightGBM, 3 shipped folds). Whether to keep only links paid in January (known on 1 February) is a question for the curator.
        - Tenure: `Tempo Emprego` counts the months to 31 December, or to the separation, so it carries the outcome (LEAK-10). We rebuild the tenure on 1 February: 11 months less for a link in post at the year's end, (m - 2) months and 0.42 of a month less for one separated in month m, floored to whole months; a January hire gets 0 (under one month on 1 February). The day of the separation is not published: 0.42 is the mean part of the month that has passed at a separation, measured over the 2025 leavers hired in January to April (their tenure to the separation against the stayers' of the same admission month). The first rebuild (half a month, rounded half to even) marked the class: January-hire leavers showed 1 or 2 months where stayers had at most 1, and the parity of the leavers' k + 0.5 values differed by class (LEAK-13); a confirmed leak goes even when small (LEAK-6), here at most 0.0005 ROC AUC. Floored, the share of even values is 0.53 for stayers and 0.49-0.50 for leavers, against 0.55 and 0.57-0.60 before. The 593 negative values of the links admitted before the year (0.03%, inconsistent records) become 0.
        - Contract type: for links with at most 3 months of tenure on 1 February, the CLT fixed-term types (60, 65, 70, 75) become their open-ended twins (10, 15, 20, 25; 27,100 links of the sample). The file keeps the year's last type, and an experience contract that survives is converted to open-ended, so for a recent hire "fixed term" marks a leaver: January hires the file shows on type 60 are 98.9% separated (37.4% quit), on type 10 45.5% (15.7%) (decision 6). The merge costs January hires 0.0175 ROC AUC (3 of 3 folds) and the whole task 0.001 (LEAK-10, LEAK-6, LEAK-7). For older links the type is stable (26% of links on 60 separate, 21% on 10).
        - Potential leak, kept on purpose: the occupation, contract type, worker category and weekly hours are the year's declared values, so a change during the year shows its later value. Linked across 2024 and 2025 in the Norte file (12 coded fields and the tenure), a year changes the occupation of 6.3% of the stayers, the hours of 3.2% and the contract type of 2.8% (an upper bound, linkage noise included). The one located part, the conversion of fixed-term contracts, is merged (above). The worker category shows no conversion: January-hire apprentices are 56.8% separated against 74.7% of the older ones, the experience contract sits in category 101 under types 60-75, and 98.4% of the temporaries' separations are their contracts' ends. The rest cannot be traced without ids (LEAK-10).
        - Dropped as recorded after the prediction point (LEAK-10): the separation reason and month, the admission month (0 or 1 in the cohort, held by the tenure), `Ind Vínculo Ativo 31/12`, `Tempo Emprego`, the December pay, the leave days of the year and `Tamanho Estabelecimento`, the establishment's active links on 31 December. That size counts this link: the class Zero is a closed workplace whose links have all ended (decision 3). The year's average pay, the pay of February to November, the leave causes and the bands of pay, age, hours and tenure are not read.
        - Dropped the worker's sex, race and colour, age, nationality, and disability (type and flag): Brazilian law (Lei 9.029/1995, art. 1, as amended by Lei 13.146/2015, in force in 2025) bars "qualquer prática discriminatória e limitativa para efeito de acesso à relação de trabalho, ou de sua manutenção" by sex, origin, race, colour, marital status, family situation, disability, professional rehabilitation and age, among others, and a retention offer (a raise, a talk, a training plan) is a practice for keeping the job, so the actor may not use them (SEL-1; the Tensions row "a factor the actor may no longer use", extended to any decision on a person where the actor's own law bars the factor, an amendment the curator confirms). They cost 0.006-0.007 ROC AUC, nearly all of it age; the other four carry at most 0.001 (3 seeds). Age was no leak: it is read at one fixed date for leavers and stayers (430,953 Norte leavers linked to their 2024 rows are a year older in 96.5-98.1% of every separation month).
        - Not read, besides: `Tipo Estabelecimento - Nome` (a copy of its code), `Ano Chegada Brasil` (1198 in every row) and the CNAE 95 class (the ministry's conversion of the declared CNAE 2.0 code into the 1995 classification: one class per CNAE 2.0 subclass on all 5,645,037 Norte links, 99999 in 201,575 of them).
        - Dropped as copies of a level of another column (CLEAN-5): `Ind CEI Vinculado` (the register type is CNO) and `Ind Trabalho Intermitente` (the worker category is the intermittent contract); each matches on every row of the sample.
        - Dropped the five codes that divide four cities (neighbourhoods of São Paulo, Fortaleza and Rio de Janeiro, districts of São Paulo, regions of the Federal District): 999997, outside the city, in every link of 2024 and 2025, the cities' own links included (CLEAN-5).
        - Proxy missing values (CLEAN-10): weekly hours 0 and 99, whose hours band is {ñ class} in every such row of the Norte file (2.3%; 74% of them general employees, 24% intermittent contracts); legal nature 9999 (2.5%); CBO 999999, CNAE 99999 and its IBGE subsector 98; the municipality's "<UF>9999" and 999999; contract type 999 and admission type 5 (undocumented, a few rows).
        - Negative January pay (1,400 links of the sample, -587,678.75 to -0.01) is set to missing: pay cannot be negative, so these are reversals of an earlier payment (CLEAN-11); their quit rate is about twice the base, a sign of an irregular link, which the missing value keeps.
        - Note: `work_municipality`, the municipality where the employee works when the employer gives one, is missing for 99.6% of the links; kept as published.
        - Note: occupation (CBO 2002), sector (CNAE 2.0 subclass and class), legal nature (CONCLA) and municipality (IBGE) ship as their codes, zero-padded text, not as words: a departure from CLEAN-12 for the curator. The release's codebook, the 2020 layout, is older than the 2025 codes: it lacks 203 occupation codes (6.4% of the rows), 29 CNAE subclasses (1.2%) and 19 legal-nature codes (11.8%; 1244, the second-largest level, among them), and it names no CNAE 2.0 class, so a decode from it would leave holes. The current official tables (the ministry's CBO list, CNAE 2.3 and natureza jurídica 2021 at IBGE CONCLA, the IBGE municipalities) would decode them into "words [code]"; whether to do so is open for the curator.
        - Decoded into the layout's words (CLEAN-12): education (an ordered scale, `EDUCATION_LEVELS`), contract type, eSocial worker category (Tabela 01), admission type, register type, IBGE subsector and the SIMPLES and part-time flags.
        - Note: `pay_january` is 0 for 11.3% of the links we keep (3.0% of those who quit, 11.9% of the others): on leave, a dormant link (above), or no pay reported for January; kept as recorded, in nominal reais.
        - Note: the cohort pools every formal link, also the statutory and other public servants and the state military (worker categories 301-310: 19.4% of the links we keep, 1.3% of whom quit, against 8.8% of the private employees, categories 101-111), whom no private HR team scores. Untuned LightGBM on the 3 shipped folds scores 0.789 ROC AUC pooled and 0.746 trained and tested on the private employees only; the order of five learners is the same (Kendall tau 1.0, 0.8 and 1.0 by fold, the one swap a near-tie), and the pooled model scores the private rows as well as one trained on them (0.746). The statutory servants and the state executive (legal nature 1023) almost never resign, the pure feature values `dataset check` reports. Shipped pooled, as the census is (USE-8); a private-only cohort is a question for the curator.
        - Note: ROC AUC (the fallback) ranks links pooled across employers and sectors, not one employer's staff, the unit the actor ranks: no employer id ships, so a score per employer cannot be computed (MET-1, MET-2). Within cells of one sector subclass and municipality, a stand-in for a workplace, the same kind of model scores about 0.73.
        - One year, IID (tag ForcedIIDFromTemporal): a real model trains on the previous year's cohort, which a temporal split mirrors, but RAIS links cannot be followed across years (no ids), so the years are cohorts, and three yearly windows with at least half the rows before each need six years (SPLIT-14). The years before 2023 are not comparable: base years 2022 and 2023 moved employers to eSocial, which the ministry calls a break in the series (SPLIT-20; MTE, RAIS 2022 technical note), and the 2023-2025 files share one layout, so the clean stretch holds one window. We ship the newest year; stacking 2024 and 2025 would put the same jobs on both sides (48% of the Norte stayers of 2025 match one 2024 row on 12 coded fields and the tenure). The random split costs little: untuned LightGBM trained on 1M links of the 2024 cohort (built and cleaned by this definition's code; 87,747,220 links, 56,388,578 in post on 1 February, 7.1% quits) scores ROC AUC 0.7829 on the three shipped test folds of 2025, against 0.7891 trained on their training folds, lower on 3 of 3 folds (log loss 0.2266 against 0.2240), with one year of training data (2023 not downloaded). About 0.004-0.005 of the gap is the year's own quits shared within a cell of sector, municipality and legal form between training and test (a workplace or a local shock), measured by holding the test rows' cells out of each year's training; the order of five learners is the same under both protocols, while learners that memorise the codes gain more from the random split (+0.010 against +0.005; measured before the panel's changes). Revisit when the post-2023 stretch holds six base years, or when linked RAIS microdata appear.
        - Duplicates kept (LEAK-18): 4.0% of the rows repeat another exactly (0.8% before the protected grounds left), different workers with identical coarse features: 66% of the repeated rows are public servants or state military of one body, 45% have no January pay, and 2.7% quit; 1,515 rows conflict in the target. 4.9-5.0% of each test fold has an exact copy in training: 4.7% of the test rows only with the same label, 0.1% only with another, 0.1% with both (leak probe); 2.4% of these rows quit.
        - Spatial: the establishment's municipality.
        - Note: the year is that of the release we use: the 2025 base-year files were posted on the FTP on 2026-05-13; RAIS microdata have been published since base year 1985.
        - Note: the gov.br page publishes its content under CC BY-ND 3.0; the FTP and its files state no licence of their own.
    """

    # Task
    target = "quit_by_year_end"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "RAIS is a labour census and defines no prediction task or score. We checked the gov.br microdata page, "
            "the PDET FTP's layouts and notice, Base dos Dados and the raisr package; a search found no study that "
            "predicts quits from RAIS with a stated metric."
        )
    )

    # Splits
    row_budget = RowBudget(train=1_000_000, test=500_000)

    prepared_raw_files = (PREPARED, PREPARED_COUNTS)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # One pass over the year's seven link files (about 23 GB of text): keep the links active on 1 February and
        # the columns we read, then draw SAMPLE_ROWS of them.
        import polars as pl

        position = {name: f"c{i}" for i, name in enumerate(HEADER)}
        exprs = [pl.col(position[c]).str.strip_chars().cast(pl.Int32).alias(a) for c, a in READ_INTEGER.items()]
        exprs += [pl.col(position[c]).str.strip_chars().cast(pl.Float64).alias(a) for c, a in READ_DECIMAL.items()]
        frames, counts = [], []
        for path in sorted((raw_dir / EXTRACTED).glob("RAIS_VINC_PUB_*.COMT")):
            with open(path, "rb") as f:
                header = tuple(h.strip('"') for h in f.readline().decode("latin-1").rstrip("\r\n").split(","))
            if header != HEADER:
                msg = f"{path.name}: the header differs from the 2023-2025 layout"
                raise ValueError(msg)
            # the header's accents are Latin-1 and the values ASCII: read the values under positional names
            lf = pl.scan_csv(path, encoding="utf8-lossy", new_columns=list(position.values()), infer_schema=False)
            links = lf.select(exprs).collect(engine="streaming")
            # the cohort: links admitted before February and not separated in January
            cohort = links.filter((pl.col("admission_month") <= 1) & (pl.col("separation_month") != 1))
            counts.append(
                {
                    "file": path.name,
                    "links": links.height,
                    "cohort": cohort.height,
                    "quits": int(cohort["separation_reason"].is_in(list(QUIT_REASONS)).sum()),
                }
            )
            frames.append(cohort)
            del links
        cohort = pl.concat(frames, how="vertical")
        del frames
        rng = np.random.default_rng(SAMPLE_SEED)
        rows = np.sort(rng.choice(cohort.height, size=SAMPLE_ROWS, replace=False))
        cohort[rows].write_parquet(raw_dir / PREPARED, compression="zstd")
        pd.DataFrame(counts).to_csv(raw_dir / PREPARED_COUNTS, index=False)

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {"links": pd.read_parquet(raw_dir / PREPARED), "counts": pd.read_csv(raw_dir / PREPARED_COUNTS)}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df = raw["links"]
        # 1. Links whose outcome the source does not record leave (LEAK-25, CLEAN-15): those it flags as abandoned (no
        #    separation, no pay in January or December) and the armed forces (no separation recorded in 2025).
        assert (df.loc[df["abandoned"] == 1, "separation_month"] == 0).all()
        df = df[(df["abandoned"] == 0) & (df["worker_category"] != ARMED_FORCES)]
        # 2. The target: a separation at the employee's initiative between February and December. Every cohort link
        #    has a separation month exactly when it has a reason, and is active on 31/12 exactly when it has neither.
        separated = df["separation_month"] > 0
        assert (separated == (df["separation_reason"] > 0)).all()
        assert (separated == (df["active_dec31"] == 0)).all()
        df[self.target] = np.where(df["separation_reason"].isin(QUIT_REASONS), "Yes", "No")
        # 3. Tenure on 1 February, in whole months. `tenure_end` counts the months to 31/12 (11 after 1 February) or
        #    to the separation, which falls in month m, (m - 2) whole months and a part of month m after 1 February:
        #    the measured mean part. Floored, not rounded half to even (which marked the class by the parity of the
        #    leavers' k + 0.5 values); a January hire has under one month (LEAK-10, LEAK-13). `+ 0.0` turns -0.0 to 0.
        elapsed = np.where(separated, df["separation_month"] - 2 + SEPARATION_DAY, 11.0)
        tenure = np.floor(df["tenure_end"] - elapsed).clip(lower=0)
        df["tenure_months"] = tenure.where(df["admission_month"] == 0, 0.0) + 0.0
        # 4. The file keeps the year's last contract type, and an experience contract that survives becomes
        #    open-ended: for recent hires, CLT fixed term marks the leavers. Merge it into its open-ended twin (LEAK-10).
        recent = df["tenure_months"] <= RECENT_HIRE_MONTHS
        df["contract_type"] = df["contract_type"].mask(recent, df["contract_type"].replace(FIXED_TERM_TO_OPEN_ENDED))
        # 5. The sub-municipal codes are empty in this release: drop them (CLEAN-5).
        assert (df[SUB_MUNICIPAL] == 999997).all().all()
        df = drop_columns(df, SUB_MUNICIPAL)
        # 6. Proxy missing values and negative January pay (a reversal, not a pay; CLEAN-11), then the codes the
        #    layouts name in words, and the classification codes as text.
        df = set_missing(df, PROXY_MISSING)
        df["pay_january"] = df["pay_january"].mask(df["pay_january"] < 0)
        for col in ("municipality", "work_municipality"):  # "<UF>9999": ignored within the state, 999999: ignored
            df[col] = df[col].mask(df[col] % 10_000 == 9_999)
        df = decode(df, CODE_LABELS)
        for col, width in CODE_WIDTHS.items():
            df[col] = df[col].astype("Int64").astype("string").str.zfill(width)
        # 7. Drop what is recorded after 1 February, the flags that copy a level of another column, and the grounds
        #    the employer may not use (SEL-1).
        return drop_columns(df, AFTER_PREDICTION_POINT + COPIES + PROTECTED_GROUNDS)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[c for c in [*CODE_LABELS, *CODE_WIDTHS] if c != "education"],
            ordinal={"education": list(EDUCATION_LEVELS.values())},
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        links = raw["links"]
        counts = raw["counts"].set_index("file")
        counts.loc["all files"] = counts.sum()
        counts["cohort share of links"] = (counts["cohort"] / counts["links"]).round(3)
        counts["quit share of cohort"] = (counts["quits"] / counts["cohort"]).round(4)
        reasons = links.groupby("separation_reason").size().rename("links in the sample").to_frame()
        reasons["label"] = ["Yes" if r in QUIT_REASONS else "No" for r in reasons.index]
        reasons["meaning (RAIS layout 2020)"] = [SEPARATION_REASONS.get(r, "not in the layout") for r in reasons.index]
        size = (
            links.assign(separated=links["separation_month"] > 0, quit=links["separation_reason"].isin(QUIT_REASONS))
            .groupby("establishment_size_dec31")[["separated", "quit"]]
            .mean()
            .round(3)
        )
        size.index = [ESTABLISHMENT_SIZES[i] for i in size.index]
        active = links[links["separation_month"] == 0]
        abandoned = active.groupby("abandoned").agg(
            links=("abandoned", "size"),
            no_pay_january=("pay_january", lambda x: round(float((x == 0).mean()), 3)),
            no_pay_december=("pay_december", lambda x: round(float((x.fillna(0) == 0).mean()), 3)),
            median_tenure_end_months=("tenure_end", "median"),
        )
        abandoned.index = ["not abandoned", "abandoned"]
        kept = links[links["abandoned"] == 0]
        group = np.select(
            [
                kept["worker_category"] == ARMED_FORCES,
                kept["worker_category"].between(301, 310),
                kept["worker_category"].between(101, 111),
            ],
            ["Military, armed forces (314)", "Public servants and state military (301-310)", "Employees (101-111)"],
            "Other categories",
        )
        armed = kept.groupby(group).agg(
            links=("worker_category", "size"),
            separated=("separation_month", lambda x: round(float((x > 0).mean()), 4)),
            quit=("separation_reason", lambda x: round(float(x.isin(QUIT_REASONS).mean()), 4)),
            no_pay_january=("pay_january", lambda x: round(float((x == 0).mean()), 3)),
        )
        january = kept[(kept["admission_month"] == 1) & kept["contract_type"].isin([10, 60])]
        contract = january.groupby(january["contract_type"].map(CONTRACT_TYPES)).agg(
            links=("contract_type", "size"),
            separated=("separation_month", lambda x: round(float((x > 0).mean()), 3)),
            separated_by_april=("separation_month", lambda x: round(float(x.between(2, 4).mean()), 3)),
            quit=("separation_reason", lambda x: round(float(x.isin(QUIT_REASONS).mean()), 3)),
        )
        return [
            Decision(
                "The cohort: links active on 1 February",
                "The prediction point is 1 February: a link admitted before February and not separated in January. "
                "Counts over the whole year's files; the sample is drawn from the cohort of all files.",
                counts,
            ),
            Decision(
                "The target: separations at the employee's initiative",
                "Codes 20 and 21 are the employee's initiative; every other separation, and no separation, is No, "
                "agreements (90) included (USE-5). Six codes of the 2023-2025 files are not in the 2020 layout and "
                "count as No.",
                reasons,
            ),
            Decision(
                "Establishment size on 31 December dropped",
                "The size class counts the establishment's active links on 31/12, this link included: the class Zero "
                "means every link has ended (LEAK-10).",
                size,
            ),
            Decision(
                "Abandoned links dropped",
                "Links flagged abandoned have no separation and no pay in January or December: their outcome is not "
                "recorded (LEAK-25). The flag is not the whole unrecorded pattern: the armed forces' outcomes are not "
                "recorded in 2025 either (decision 5).",
                abandoned,
            ),
            Decision(
                "Armed forces (worker category 314) dropped",
                "In 2025 the armed forces record 3 separations in their 418,633 links of the seven files, against 254 "
                "of 12,651 links (2.0%) in the 2024 sample built by this code, and 85% of their links have no January "
                "pay, against 3.3% in 2024: a change in the recording, not in behaviour, so their No is not recorded "
                "(LEAK-25). The sample, after the abandoned links:",
                armed,
            ),
            Decision(
                "CLT fixed term merged into open-ended for recent hires",
                "The file keeps the year's last contract type, and an experience contract (CLT fixed term) that "
                "survives is converted to open-ended. Among the January hires of the sample, those the file shows on "
                "fixed term have almost all left: the type marks the leavers. For links with up to 3 months of tenure "
                "on 1 February, types 60, 65, 70 and 75 become 10, 15, 20 and 25 (LEAK-10).",
                contract,
            ),
        ]
