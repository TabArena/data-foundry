"""Curated dataset definition for `pricing_game_2016_french_fleet` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    SplitPlan,
    TaskSummary,
    Temporal,
    drop_columns,
)

# The organisers' French column names, renamed after their descriptions in the game's rules (pricing-game-2016-FR.pdf,
# Sec. 1); CASdatasets' names for the same columns are in its pricingame.Rd.
RENAME = {
    "Num_contrat": "contract_id",  # "Numéro d'affaire"
    "IMMAT": "vehicle_id",  # "Immatriculation"
    "Date_Deb_Situ": "period_start",  # "Date de début de situation"
    "ANNEE": "year",  # "Année de situation"
    "Date_Fin_Situ": "period_end",  # "Date de fin de situation"
    "Classe_Age_Situ_Cont": "contract_age_class",  # "Classe age du contrat"
    "Type_Apporteur": "distribution_channel",  # "Type d'apporteur (agents ou courtiers ou autres)"
    "Creation_Entr": "new_company",  # "Indicateur de création entreprise (à 2 si création)"
    "Mode_gestion": "fleet_management",  # "Mode de gestion de la flotte"
    "Activite": "client_activity",  # "Activité du client (niveau contrat)"
    "Zone": "zone",  # "Zone géographique"
    "Segment": "fleet_size_class",  # "Taille de la flotte"
    "Fractionnement": "payment_frequency",  # "Fractionnement de paiement de la prime"
    "Exposition_au_risque": "exposure",  # "Véhicules année (exposition au risque)"
    "Age_du_vehicule": "vehicle_age_class",  # "Classe d'âge du véhicule"
    "ValeurPuissance": "power_value_class",  # "Combiné puissance valeur du véhicule"
    "franchise": "deductible_class",  # "Classe de franchise de la garantie DTA"
    "Nombre_vehicule": "n_vehicles",  # "Nombre de véhicule"
    "Valeur_assuree": "insured_value_class",  # "Valeur assurée"
    "FORMULE": "formula",  # "Formule souscrite"
    "Categorie_ensemble": "vehicle_category",  # "Catégorie du véhicule"
    "nombre_de_sinistre": "claim_count",  # "Nombre de sinistres"
}
# A claim's period: the contract, the vehicle, the year and the period's dates (every claim joins one period).
CLAIM_KEYS = ["Num_contrat", "IMMAT", "ANNEE", "Date_Deb_Situ", "Date_Fin_Situ"]
TARGET = "claim_charge"
CATEGORICAL = [
    "contract_age_class",
    "distribution_channel",
    "new_company",
    "fleet_management",
    "client_activity",
    "zone",
    "fleet_size_class",
    "payment_frequency",
    "vehicle_age_class",
    "power_value_class",
    "deductible_class",
    "insured_value_class",
    "formula",
]
# The test windows: the periods starting in 2013, in thirds of the year, newest first; each window trains on the
# periods closed before it starts (an expanding train side, the curator's call of 2026-11-02).
WINDOWS = (("2013-09-01", "2014-01-01"), ("2013-05-01", "2013-09-01"), ("2013-01-01", "2013-05-01"))
# The game's rules (the columns in Sec. 1, the market in Sec. 4).
RULES_URL = "http://web.archive.org/web/20210422004748/https://freakonometrics.hypotheses.org/files/2016/08/pricing-game-2016-FR.pdf"


class PricingGame2016FrenchFleet(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What will a vehicle of a French company's fleet cost in material-damage claims over a period of cover, "
            "from the contract's and the vehicle's rating classes and the length of cover to the year's end, known at "
            "the start?"
        ),
        use_case=(
            "A fleet insurer setting its tariff: it fits the pure premium, the expected claim cost per vehicle and "
            "period, on the periods closed so far and prices each fleet vehicle's cover with it. The 2016 actuarial "
            "pricing game posed this pricing task on this portfolio."
        ),
        row=(
            "One vehicle of a fleet contract over one period with unchanged contract terms, cut at each change and at "
            "the year's end: 87,228 periods of 68,485 vehicles in 18,037 contracts of an unnamed French insurer, "
            "2011 to 2013."
        ),
        predicted=(
            "The period's claim charges summed (0 for 95.7% of the periods), net of the flat amounts recovered under "
            "the IDA convention between insurers, where the insurer pays its client and recovers a flat amount from "
            "the other insurer; a net recovery counts as 0. The charges are scaled by one constant of the release."
        ),
        known=(
            "The contract's age, the client's activity, zone, fleet size and management, a new-company flag, the "
            "distribution channel, payment frequency, formula, deductible and insured value classes; the vehicle's "
            "age and power-value classes; the period's start date and the length of cover to the year's end, known "
            "at the start. Most periods end earlier, at a cut nobody scheduled, which is not known then."
        ),
        split=(
            "Tested on the periods starting in 2013 in three four-month windows, each trained on every period closed "
            "before the window starts, as a tariff refit every four months; most fleets of 2013 were insured before."
        ),
        changes=(
            "We summed each period's claim charges and set the 537 net negative totals to 0, replaced the period's "
            "realised length by its length to the year's end, dropped the identifiers, the year and the period's end "
            "date, made the unknown insured value missing, and gave two codes their labels."
        ),
        fit="direct",
        fit_reason=(
            "The rows are the periods an insurer prices, the features the rating classes and the length of cover it "
            "knows then, and each test window follows its training side. The target sums the claims over the cover "
            "the vehicle kept, so it also holds how long the vehicle stays, which the insurer can only expect at "
            "pricing; the signal is in the claim frequency."
        ),
    )

    # Dataset
    unique_name = "pricing_game_2016_french_fleet"
    year = "2016"
    domain = "insurance"
    source = "Other"  # the organisers' files on Arthur Charpentier's site; no closer schema value
    source_url = "https://actinfo.hypotheses.org/69"
    license = None  # none stated by the organisers; CASdatasets, which redistributes the tables, is GPL (>= 2)
    data_tags = ("Anonymized", "Spatial")
    download_description = """
        The second actuarial pricing game (Arthur Charpentier, Romuald Elie and Jérémie Jakubowicz, for the 100% Data
        Science day of the Institut des Actuaires on 8 November 2016; announced on https://actinfo.hypotheses.org/69,
        DOI 10.58079/al7p) gave its players three CSV files, still on the organiser's site (Last-Modified 13 July
        2016) and archived by the Wayback Machine on 12 September 2025 with the same bytes. The rules describe the
        columns: http://web.archive.org/web/20210422004748/https://freakonometrics.hypotheses.org/files/2016/08/pricing-game-2016-FR.pdf.
        We use the two training files; test_contrats.csv (the 32,772 periods of 2014 to price) has no claims.
        The R package CASdatasets holds the same tables, renamed and recoded, as pg16trainpol, pg16trainclaim and
        pg16test (man/pricingame.Rd); its DirectComp column disagrees with the organisers' IDA flag on 1,064 claims.

        mkdir -p local-data-warehouse/pricing_game_2016_french_fleet && cd local-data-warehouse/pricing_game_2016_french_fleet
        for f in train_contrats train_sinistres; do wget http://freakonometrics.free.fr/pricinggame/$f.csv; done
        # or: wget -O $f.csv http://web.archive.org/web/20250912080148id_/http://freakonometrics.free.fr/pricinggame/$f.csv
        sha256sum train_contrats.csv train_sinistres.csv
        # d0f9caeb8146a03bdfe8ef67be2a5df576f35ae31a34d91f4c10946885c4f14a  train_contrats.csv
        # d41f7b18afea4767c50d750909be669c272696fd9d75587ca83a00d1ce6e45fe  train_sinistres.csv
    """
    bibtex = r"""
        @misc{Charpentier2016PricingGame,
          author = {Charpentier, Arthur and Elie, Romuald and Jakubowicz, J{\'e}r{\'e}mie},
          title = {Pricing Game 100\% Data Science},
          year = {2016},
          howpublished = {\url{https://actinfo.hypotheses.org/69}},
          note = {Second actuarial pricing game, Institut des Actuaires, 100\% Data Science day of 8 November 2016;
            data files train\_contrats.csv and train\_sinistres.csv at http://freakonometrics.free.fr/pricinggame/;
            DOI 10.58079/al7p; distributed as pg16trainpol and pg16trainclaim in the R package CASdatasets (Dutang
            and Charpentier)}
        }
    """
    curation_comments = """
        We start with train_contrats.csv and train_sinistres.csv, the files the organisers of the second actuarial pricing game (2016) gave its players.

        - Prediction point: the start of a vehicle's period of cover, when the insurer prices it with the year's tariff, fit on the closed years. The game asked for "une prime pure" (a pure premium) for each of the 32,772 periods of 2014 in test_contrats.csv (rules, Sec. 2, which write 37,772), with the periods of 2011 to 2013 to learn from; the period's claim charge is what a pure premium predicts. Known then: the contract's and the vehicle's rating classes, the period's start and its length of cover to the year's end. Not known: the period's claims, and when a period cut short will end.
        - Source and year: the game's page (actinfo.hypotheses.org/69, 17 July 2016) dates the first stage "entre le 15 juillet et le 15 septembre", and the files carry a Last-Modified date of 13 July 2016. The rules (pricing-game-2016-FR.pdf, Sec. 1) describe every column; CASdatasets' copy holds the same values, its levels renamed one to one, except its DirectComp, which is 0 for 1,064 of the 1,190 claims the organisers flag IDA (a problem of that copy, not used here).
        - The portfolio is commercial fleets with a material-damage cover, not the "private motor insurance" of CASdatasets' documentation: the rules describe "Mode de gestion de la flotte", "Taille de la flotte" and "Classe de franchise de la garantie DTA" (DTA is the usual French abbreviation of an all-accident damage cover), and 1,190 of the 4,568 claims fall under the IDA convention between insurers. The row names of the training file and the 2014 file together run exactly from 1 to 120,000, so the files are likely a sample of the portfolio: counts per contract (at most 12 vehicles of a contract at once) and a vehicle's last period describe the file, not the fleets.
        - Target `claim_charge`: the charges (CHARGE_SINISTRE) of the period's claims summed, 0 without a claim. Each of the 4,568 claims joins one period on the contract, the registration, the year and the period's dates, and the claim count equals the joined claims on every period (checked in `_load_raw`). 4,250 periods have a claim (286 two or more, at most 7); 3,711 have a positive total (median 1,339, at most 13,992), so 95.7% of the targets are 0. The curator first chose the claim indicator (2026-10-30, record) and switched to the charge on 2026-11-02, after a measurement: the charge is what the insurer prices and what the game asked for, and the family's amount targets (fremtpl2, frempl, pricing_game_2017_french_mtpl) keep it.
        - 537 periods net below 0 set to 0 (down to -1,863), as pricing_game_2017_french_mtpl and frempl_french_motor_personal_line do (the family call of 2026-10-30: "a net recovery is no claim cost of the year"). They are claims under the IDA convention ("1 si sinistre Indemnisation Direct de l'Assuré", rules Sec. 1), where the insurer pays its client and recovers a flat amount, not the cost, from the other insurer; every claim with a charge of 0 or less is IDA, and 126 of the 1,190 IDA claims are at 50% responsibility. Tweedie and Poisson losses need a non-negative target. The total is clipped, not each claim (65 periods mix signs, 16 of them net below 0); the clip raises the total claim cost by 4.3%.
        - Only the frequency carries signal. Among the periods with a positive charge, the log charge is not predictable from the classes (R^2 -0.06 for LightGBM, -0.02 for ridge, measured on 2011-2012 to 2013), and a Poisson model of the claim count ranks the charges as well as models of the charge do (normalized Gini 0.202, 0.271, 0.279 on the windows, against 0.155, 0.245, 0.276 for a Tweedie LightGBM). The task is the frequency task with severity noise on top. Raw charge, not log1p: the normalized Gini ranks by the expected cost, as in pricing_game_2017_french_mtpl.
        - `exposure` is the length of cover known at the period's start, in vehicle-years ("Véhicules année (exposition au risque)"): (31 December - start + 1) / 365, / 366 in the leap year 2012, times the period's vehicles (2 on two periods), rounded to 0.01 (LEAK-10, LEAK-7). The source's value is the realised length, the same formula to the period's end (it matches on every period). 57.4% of the periods (57.9% in 2013) end before 31 December at a cut nobody scheduled, 0.8% at a contract anniversary, so their length is known only at their end, and with `period_start` a feature it gave back the dropped end. On the three windows the realised length added ROC AUC on the claim indicator +0.040, +0.055 and +0.052 over the length known at the start (regularised LightGBM on the rating classes and the start's day of the year, 3 seeds), and the early ends go with claims: a rate ratio of 1.22 [1.12, 1.33] given the rating classes (Poisson GLM with the length as offset, 2011-2012). The new length follows from the start date and stays as the time at risk a frequency model takes as given. Confirmed by the curator (Andrej, 2026-11-02) and recorded as the LEAK-10 case for time on risk cut short by the outcome: the cut is fixed where the data locates it.
        - The covariates add to the length: on the three windows (newest first) the length alone ranks the charges at normalized Gini 0.101, 0.150 and 0.066, a Tweedie GLM on all features at 0.167, 0.270 and 0.268, a regularised Tweedie LightGBM (3 seeds) at 0.155, 0.245 and 0.276 (bootstrap standard errors 0.071, 0.043 and 0.023). The models beat the time at risk on every window, so the task is not trivial (TP-4), though on the newest window (103 positive charges) only by about one standard error. An untuned squared-error LightGBM scores 0.006, 0.226 and 0.253: on the newest window it does not beat the length. On the claim indicator the same split gives ROC AUC 0.550, 0.568 and 0.529 for the length against 0.597, 0.622 and 0.652. The task probes flag `no_signal` and `drift_baseline` (TP-1, TP-2): they score R^2, which follows a few large charges (best family linear, R^2 0.001); under the declared Gini the models beat the length on every window, as for pricing_game_2017_french_mtpl. The leak probes find nothing (every feature alone at R^2 -0.001 or below, 2.9% of the test rows with a feature copy in training).
        - Not added, measured on all of 2013 on the claim indicator (the same LightGBM, trained on 2011-2012): the contract's and the vehicle's claims and exposure of the previous year (ROC AUC 0.667 with them, 0.668 without; a known entity's history is legitimate, USE-10, but it carries nothing here), and the contract's vehicles in force at the period's start (0.667).
        - Dropped: `contract_id` (apparently numbered in the order of subscription: median 14,885 for contracts of at most a year, 2,027 for those over 5 years, which the contract's age class carries) and `vehicle_id` (the anonymised registration), `year` (the year of the period's start on every row), `period_end` (unknown at the start for the periods that end early; it only sets each window's training side), `vehicle_category` (one value) and the files' unnamed row index.
        - `insured_value_class` "ND" (not available) made missing: 87,093 periods (99.8%); the 135 others hold five value classes.
        - Labels restored: `payment_frequency` A, S, T as annual, semi-annual, quarterly (the French "annuel", "semestriel", "trimestriel"); `new_company` 2 as Yes and 1 as No ("à 2 si création", rules Sec. 1). The other classes keep the organisers' codes: French labels for the ages and the deductible, anonymised numbers for the zone, activity, channel, formula, fleet size and power-value class.
        - Dtypes: every class column categorical; the power-value class (11 levels, a combined power and value grid) has no documented order. `exposure` and `n_vehicles` numeric (`n_vehicles` is 1 on every period but 2, which hold 2; kept as the source ships it); `period_start` a date.
        - 11,807 periods (13.5%) repeat the features of another, 10,828 of them with the same target and 979 with another: vehicles of one fleet in the same period share every contract class and the start, so the length, and differ only by their own two classes. Natural, kept (LEAK-18).
        - Anomaly: no period is shorter than 30 days, in the training file and the 2014 pricing file alike, and no period of a year starts after 2 December: the organisers seem to have left the shortest periods out, so the task covers periods of a month or more.
        - Anomaly: the categorical levels are anonymised and the charges scaled by one constant (the record's generated-data tests of 2026-11-01: disclosure control, not generation); the charges are kept as published (the constant, 1.077841, changes no ranking).
        - The newest periods lose no claims: claims per vehicle-year are 0.117, 0.119 and 0.119 in 2011 to 2013, and 0.115, 0.114 and 0.117 for the periods ending in the fourth quarter (LEAK-24 not triggered).
        - Note: claims of the periods that close just before a window starts may have been reported only after the refit. The files hold the counts as of their extract (claims closed up to 2014, 41 still open) and no report date, so the delay can only be simulated: hiding the training charges whose claim falls in the last 30 or 90 days before each window's start (each claim placed uniformly in its period; 100 and 318 positive periods for the January window, at most 70 for the others) leaves the mean normalized Gini over the windows at 0.225 and 0.226 against 0.225 (regularised Tweedie LightGBM, 3 seeds). 41 claims were still open at the extract, so their charges may still move. A simulation, not a measurement. No gap separates the sides: an exception to SPLIT-10 that serves SPLIT-14 (Andrej, 2026-11-02), since rows are cut at 31 December and even a 1-day gap before the January window leaves 50.2% of the rows in training, a month 48.7%.
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.stand_in(
        "normalized_gini",
        original=(
            "each player's result in the 2014 market the organisers ran as a price aggregator: each insured going to "
            "a company drawn at random among the cheapest premiums, every player's premiums scaled by one uniform "
            "factor to a total of 2.5 million euros (rules, Sec. 4 'Règles du Jeu')"
        ),
        reason=(
            "The market needs the other players' premiums and the claims of 2014, neither published. The uniform "
            "scaling ('un facteur d'inflation appliqué uniformément') took away each player's price level, so the "
            "market rewarded the ranking of the risks; the normalized Gini scores that ranking of the claim cost, the "
            "stand-in of pricing_game_2017_french_mtpl and the metric of the insurers' Kaggle competitions. The game's "
            "page (actinfo.hypotheses.org/69) and CASdatasets' pricingame.Rd name no other metric. The period's "
            "length carries part of the score: the length to the year's end alone ranks the charges at 0.101, 0.150 "
            "and 0.066 on the three windows, a regularised Tweedie LightGBM on all features at 0.155, 0.245 and "
            "0.276. Tweedie deviance does not separate the models on these windows."
        ),
        reference=RULES_URL,
    )
    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "Vehicles of one fleet in the same period share every contract class and the start, so the length, and "
            "differ only by their own two classes: natural repeats (LEAK-18). With `period_start` a feature no copy "
            "crosses the split."
        ),
        "dataset_conflicting_duplicate_rows": (
            "The same repeats as dataset_duplicate_rows: vehicles of one fleet with the same classes in the same "
            "period, with different claim charges. Natural (LEAK-18); the outcome of one vehicle is not the "
            "other's."
        ),
        "task_target_value_dominant": (
            "Zero-inflated by nature: the claim charge is 0 for 95.7% of the periods, those with no claim (95.1%) or "
            "whose claims net to 0 or less after IDA recoveries (0.6%, negative totals set to 0); not a cap or a "
            "placeholder."
        ),
        "meta_license_unknown": (
            "The organisers state no licence for the game's files; CASdatasets, which redistributes the same tables, "
            "is GPL (>= 2)."
        ),
    }
    temporal = Temporal(on="period_start", horizon=4, horizon_unit="months")
    splits_comment = """
        Three test windows, the periods starting in 2013 by thirds of the year (September to December, May to August,
        January to April, newest first). Each window trains on every period closed before it starts: 67,886, 61,797
        and 56,178 periods (78%, 71% and 64% of the rows), so the January window trains on 2011-2012 and the later ones
        add the 2013 periods already closed. A period still open at a window's start is in neither side (SPLIT-9). The
        use case is a tariff: the game priced every period of 2014 from 2011-2013, and the claims of 2014 were never
        published, so 2013 is the test year (suggested on 2026-10-30 and accepted with the curator's Yes). The game's
        tariff was fit once for the year; three windows that share that one training side would be one evaluation, so
        each window is a refit four months apart, which keeps three windows on distinct training sides (SPLIT-14 as
        amended and SPLIT-11, Andrej, 2026-11-02). The 2013 periods closed before a window are the ones cut short (3.2%
        and 2.4% with a claim, against 4.9% overall), as a refit on that day would see them; against the training side
        held at 2011-2012 the regularised LightGBM's ROC AUC on the claim indicator moves by at most 0.002, the untuned one loses 0.014 on the newest
        window (0.580 to 0.566, within its standard error). Three windows, not the nine of the convention (SPLIT-15):
        finer windows only cut the same test rows into noisier pieces. Rows are cut at 31 December, so a period's start
        caps its length and each window holds one cohort of lengths: most periods start on 1 January (12,028), and the
        claims per vehicle-year are flat across the windows (0.117, 0.122, 0.129), but the share of periods with a
        claim falls with the length (6.0%, 3.9%, 2.3%). A window's score ranks the periods within its cohort, and the
        mean over the windows runs below a score pooled over 2013 (ROC AUC on the claim indicator 0.626 against 0.669, an untuned LightGBM on the
        training side held at 2011-2012). The newest window is the smallest and the noisiest (5,312 periods, 123 with a
        claim, 103 with a positive charge). No gap separates the sides (SPLIT-10; the notes give the reason and the simulated bound). Fleets and
        vehicles recur across the cutoff, as a tariff prices the insurer's known fleets (SPLIT-13): 81-84% of the test
        periods belong to a contract in training, 26-30% to a vehicle in training.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        periods = pd.read_csv(raw_dir / "train_contrats.csv", index_col=0)
        claims = pd.read_csv(raw_dir / "train_sinistres.csv", index_col=0)
        assert not periods.duplicated(CLAIM_KEYS).any()
        # Each claim's period, on the contract, the registration, the year and the period's dates (the join of
        # CASdatasets' own check: every claim has a period, and the count equals the joined claims).
        per_period = claims.groupby(CLAIM_KEYS, sort=True).agg(
            joined_claims=("CHARGE_SINISTRE", "size"),
            claim_total=("CHARGE_SINISTRE", "sum"),
            claims_positive_charge=("CHARGE_SINISTRE", lambda s: int((s > 0).sum())),
            claims_ida=("IDA", "sum"),
        )
        raw = periods.merge(per_period.reset_index(), on=CLAIM_KEYS, how="left", validate="one_to_one")
        raw = raw.fillna({"joined_claims": 0, "claim_total": 0.0, "claims_positive_charge": 0, "claims_ida": 0})
        assert raw["joined_claims"].sum() == len(claims)
        assert (raw["joined_claims"] == raw["nombre_de_sinistre"]).all()
        return raw

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. English names after the rules' descriptions (RENAME).
        df = raw.rename(columns=RENAME)
        # 2. The target: the period's claim charges summed, a net negative total (IDA recoveries) set to 0.
        df[TARGET] = df["claim_total"].clip(lower=0)
        # 3. The period's start as a date; it orders the rows and sets the test windows.
        df["period_start"] = pd.to_datetime(df["period_start"], format="%d/%m/%Y")
        assert (df["period_start"].dt.year == df["year"]).all()
        # 4. The length of cover known at the period's start (LEAK-10, LEAK-7): to 31 December, in vehicle-years
        #    (days / 366 in 2012) times the period's vehicles, rounded as the source rounds. The source's exposure is
        #    the realised length, equal to this on the periods that end on 31 December; the others end at a cut
        #    known only when it comes.
        start = df["period_start"]
        year_end = pd.to_datetime(start.dt.year.astype(str) + "-12-31")
        days_in_year = np.where(start.dt.is_leap_year, 366, 365)
        to_year_end = (((year_end - start).dt.days + 1) / days_in_year * df["n_vehicles"]).round(2)
        ends_year = pd.to_datetime(df["period_end"], format="%d/%m/%Y") == year_end
        assert np.isclose(to_year_end[ends_year], df.loc[ends_year, "exposure"]).all()
        df["exposure"] = to_year_end
        # 5. Labels for two codes: the payment frequency (annuel, semestriel, trimestriel) and the new-company flag
        #    ("à 2 si création").
        df["payment_frequency"] = df["payment_frequency"].map({"A": "annual", "S": "semi-annual", "T": "quarterly"})
        df["new_company"] = df["new_company"].map({1: "No", 2: "Yes"})
        assert df[["payment_frequency", "new_company"]].notna().all().all()
        # 6. The insured value "ND" (not available): missing.
        df["insured_value_class"] = df["insured_value_class"].replace("ND", np.nan)
        # 7. The period's end, for the split only: a window trains on the periods closed before it starts.
        df["period_end"] = pd.to_datetime(df["period_end"], format="%d/%m/%Y")
        # 8. Drops: the identifiers, the year (the start's year), the constant vehicle category, the claim count and
        #    the join's columns (the target). The period's end leaves in the split step (unknown at the start when the
        #    period ends early).
        assert df["vehicle_category"].nunique() == 1
        return drop_columns(
            df,
            [
                "contract_id",
                "vehicle_id",
                "year",
                "vehicle_category",
                "claim_count",
                "claim_total",
                "joined_claims",
                "claims_positive_charge",
                "claims_ida",
            ],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=CATEGORICAL, datetime=["period_start", "period_end"])

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        """Three windows of 2013 (newest first), each trained on every period closed before the window starts."""
        start, end = df[self.temporal.on], df["period_end"]
        splits = {}
        for split, (lo, hi) in enumerate(WINDOWS):
            train = np.flatnonzero(end < pd.Timestamp(lo)).tolist()
            test = np.flatnonzero((start >= pd.Timestamp(lo)) & (start < pd.Timestamp(hi))).tolist()
            splits[split] = {0: (train, test)}
        return SplitPlan(splits=splits, df=df.drop(columns=["period_end"]))

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        periods = raw.assign(
            start=pd.to_datetime(raw["Date_Deb_Situ"], format="%d/%m/%Y"),
            end=pd.to_datetime(raw["Date_Fin_Situ"], format="%d/%m/%Y"),
            claim=raw["nombre_de_sinistre"] > 0,
        ).sort_values(["Num_contrat", "IMMAT", "start"], kind="stable")
        later = periods.groupby(["Num_contrat", "IMMAT"])["start"].shift(-1).notna()
        year_end = (periods["end"].dt.month == 12) & (periods["end"].dt.day == 31)
        ending = pd.Series(
            np.select(
                [year_end, later],
                ["31 December", "earlier, the vehicle goes on"],
                "earlier, the vehicle's last period in the file",
            ),
            index=periods.index,
            name="the period ends",
        )
        closed = periods["ANNEE"] < 2013
        rates = (
            periods.loc[closed]
            .groupby(ending[closed])
            .agg(
                periods=("claim", "size"),
                vehicle_years=("Exposition_au_risque", "sum"),
                claims=("nombre_de_sinistre", "sum"),
            )
            .rename(columns={"vehicle_years": "vehicle-years (realised)"})
        )
        rates["claims per vehicle-year"] = (rates["claims"] / rates["vehicle-years (realised)"]).round(3)
        rates["vehicle-years (realised)"] = rates["vehicle-years (realised)"].round().astype(int)
        positive = periods.loc[periods["claim"]]
        kinds = pd.Series(
            {
                "periods with a claim": len(positive),
                "with two or more claims": int((positive["nombre_de_sinistre"] >= 2).sum()),
                "with an IDA claim": int((positive["claims_ida"] > 0).sum()),
                "with no claim of positive charge": int((positive["claims_positive_charge"] == 0).sum()),
                "with a net total below 0 (set to 0)": int((positive["claim_total"] < 0).sum()),
            },
            name="periods",
        )
        return [
            Decision(
                "The period's length is the one known at its start",
                "The source's length is realised: a period that ends before 31 December is known only at its end, "
                "and 57.4% of the periods end at a cut nobody scheduled. Those ends go with claims: in 2011-2012 a "
                "vehicle's last period in the file that ends early has more claims per vehicle-year than a period "
                "that runs to the year's end (a rate ratio of 1.22 given the rating classes). `exposure` is "
                "therefore the length to 31 December for every period (curation_comments).",
                rates,
            ),
            Decision(
                "A net recovery counts as no cost",
                "The target is the period's claim charges summed. Claims under the IDA convention, where the insurer "
                "pays its client and recovers a flat amount from the other insurer, can net below 0; such a total is "
                "set to 0, as in pricing_game_2017_french_mtpl and frempl_french_motor_personal_line.",
                kinds,
            ),
        ]
