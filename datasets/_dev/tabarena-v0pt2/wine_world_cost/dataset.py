"""Curated dataset definition for `wine_world_cost` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, Metric, Source, TaskSummary

# The producer of each wine, the group of the split. The data have no producer column: the rule reads it from the
# title, and the two tables below fix what the rule gets wrong. Every one of the 1,277 titles was checked by hand
# (2026-11-11); see the curation comments for what one producer is.
_STYLE_WORDS = {
    "brut",
    "champagne",
    "prosecco",
    "cava",
    "cremant",
    "crémant",
    "rosé",
    "rose",
    "red",
    "white",
    "blanc",
    "rouge",
    "sparkling",
    "organic",
    "reserve",
    "réserve",
    "riserva",
    "reserva",
    "gran",
    "grand",
    "cru",
    "premier",
    "1er",
    "classico",
    "superiore",
    "doc",
    "docg",
    "aoc",
    "igt",
    "rioja",
}
# Titles whose first words are not the producer: an appellation, a second wine or a brand first. Matched on the start of
# the title, before the rule.
_PRODUCER_BY_TITLE_START = {
    "10 year old Malmsey Henriques": "henriques & henriques",
    "Apostoles 30-Year-Old Palo Cortado Sherry Gonzalez Byass": "gonzalez byass",
    "Barbaresco 2019/20 De Forville": "de forville",
    "Chablis 1er Cru Vaillons 2020/21 Séguinot-Bordet": "séguinot-bordet",
    "Chassagne-Montrachet Blanc 2020/21 Château de la Maltroye": "château de la maltroye",
    "Côtes-du-Rhône Villages Laudun 2017 Château Courac": "château courac",
    "Guidalberto 2020/21 Tenuta San Guido": "tenuta san guido",
    "Le Difese Tenuta San Guido": "tenuta san guido",
    "Sassicaia ": "tenuta san guido",  # Guidalberto's copy names Sassicaia as the winery's own wine
    "Montepulciano d'Abruzzo 2020/21 Masciarelli": "masciarelli",
    "Morellino di Scansano Organic Poggioargentiera": "poggioargentiera",
    "Puligny-Montrachet 2019/20 Doudet Naudin": "doudet-naudin",
    "Puligny-Montrachet 1er Cru 'La Garenne' 2015 Duc de Magenta, Jadot": "louis jadot",
    "Rasteau 'L'Andéol' 2019/20 Famille Perrin": "famille perrin",
    "Rioja Reserva Marques de Riscal": "marqués de riscal",
    "Rioja Reserva Viña Ardanza 2015/16 Magnum, La Rioja Alta": "la rioja alta",
    "Rioja Crianza Boyante": "boyante",
    "Rosé d'Anjou 'Feu!' 2020/21 Les Caves de la Loire": "les caves de la loire",
    'Sancerre Rouge "Les Bonnes Bouches" 2018/19, Henri Bourgeois': "henri bourgeois",
    "Saint-Véran Les Vignerons des Grandes Vignes": "les vignerons des grandes vignes",
    "Touraine Gamay 2020 Domaine Roc de Châteauvieux": "domaine roc de châteauvieux",
    "Vino Nobile Di Montepuliciano 2017/18 Bonacchi": "bonacchi",
    "Viré-Clessé Vieilles Vignes 2020/22 Christophe Cordier": "domaine cordier père et fils",
    "Vouvray Sec 'Expresion de Silex'": "denis meunier",  # its copy names the grower
    "Marsala Fine Curatolo Arini": "curatolo arini",
    "Dogajolo Carpineto": "carpineto",
    "Primitivo 'Il Feudo'": "il feudo",
    # second wines: the copy names the château
    "Amiral de Beychevelle": "château beychevelle",
    "Brio de Cantenac Brown": "château cantenac brown",
    "Castelnau de Suduiraut": "château suduiraut",
    "Charmes de Kirwan": "château kirwan",
    "L'Ouest de Lamothe Guignard": "château lamothe-guignard",
    "La Réserve de Léoville-Barton": "château léoville barton",
    "Baron de Boutisse": "château recougne",  # "from the family behind Château Recougne"
    # one rough key for several producers
    "Chateau de Pitray": "château de pitray",
    "Chateau l'Hyverniere": "château l'hyvernière",
    "Château Grand Faurie La Rose": "château grand faurie la rose",
    "Château Grand Jean": "château grand jean",
    "Château d'Anglès": "château d'anglès",
    "Château d’Estoublon": "château d'estoublon",
    "Château de Chassagne-Montrachet": "domaine bader-mimeur",  # Bader-Mimeur's copy: the family owns the château
    "Domaine Bader-Mimeur": "domaine bader-mimeur",
    "Caves des Grand Crus Blancs": "caves des grands crus blancs",
    "La Garnacha Salvaje del Moncayo": "proyecto garnachas de españa",  # the range of La Garnatxa Fosca's title
    "Managers' Choice: Agenda": "agenda",
    "Managers' Choice: VIK": "vik",
    "Managers’ Choice: Zocker": "zocker",
}
# Rough keys (from the rule below) that are spelling variants, name forms, ranges or brands of one producer, named so in
# the title or the shop's copy.
_PRODUCER_MERGE = {
    "aperol aperitivo 70cl": "aperol",
    "chandon garden spritz": "chandon",
    "chateau de targé": "château de targé",
    "nos terroirs bios vacqueyras": "nos terroirs bios",
    "villarei albariño": "villarei",
    "pierre gaillard domaine madeloc": "pierre gaillard",
    "three choirs stonebrook": "three choirs",
    "la garnatxa fosca": "proyecto garnachas de españa",
    # brands whose copy names the house that makes them
    "elysium": "andrew quady",  # "made by Andrew Quady"
    "armand de brignac": "cattier",  # "from 13th-generation wine growers, the Cattier family"
    "naudin père et fils": "doudet-naudin",  # "Doudet-Naudin was founded in 1849"
    "gabriel allard": "les grandes serres",  # "Les Grandes Serres winery ..."
    "rémy ferbras": "les grandes serres",
    "remy ferbras": "les grandes serres",
    "la brise blanche": "les vignobles foncalieu",  # "made by Les Vignobles Foncalieu"
    "les saules vacqueyras": "union des vignerons des côtes du rhône",
    "aimé arnoux": "domaine aimé arnoux",
    "alain grignon carignan": "alain grignon",
    "alamos lujan de cuyo": "alamos",
    "allegrini amarone della": "allegrini",
    "anna": "anna's way",
    "antinori": "antinori",
    "villa antinori": "antinori",
    "araldica barbera d": "araldica",
    "araldica moscato d": "araldica",
    "baron edmond de rothschild montagnesaintémilion": "baron edmond de rothschild",
    "bienbebido pulpo albariño": "bienbebido",
    "bodegas care garnacha blanca nativa": "bodegas care",
    "bodegas caro amancaya": "bodegas caro",
    "bodegas hidalgo": "hidalgo",
    "hidalgo manzanilla sherry la gitana 50cl": "hidalgo",
    "bodegas muga": "muga",
    "torre muga": "muga",
    "olarra clásico": "bodegas olarra",
    "bollinger rd": "bollinger",
    "bollinger special cuvée": "bollinger",
    "the bolney estate pinor": "bolney estate",
    "bostavan winery 47n": "bostavan",
    "bruce jack wines reserve collection": "bruce jack",
    "cantine maschio extra dry": "cantine maschio",
    "maschio conegliano extra dry": "cantine maschio",
    "capaia one": "capaia",
    "casa de vila nova filipa de lencastre alvarinho": "casa de vila nova",
    "castello banfi rosso di montalcino": "castello banfi",
    "catena": "catena zapata",
    "cave vinicole de hunawihr kuhlmannplatz": "cave vinicole de hunawihr",
    "caves d": "château d'esclans",  # Caves d'Esclans, Whispering Angel
    "château d": "château d'esclans",  # Garrus, Rock Angel; d'Anglès and d'Estoublon are matched by title first
    "sacha lichine": "château d'esclans",  # "the man behind the iconic Whispering Angel"
    "the pale": "château d'esclans",  # "Sacha Lichine took over Château d'Esclans ... He's turned his attention to ... The Pale"
    "cave des vignerons de buxy": "cave des vignerons de buxy",
    "caves des vignerons de buxy": "cave des vignerons de buxy",
    "chapel down english": "chapel down",
    "chapel down flint dry": "chapel down",
    "château de crezancy": "château de crézancy",
    "château de la cour d": "château de la cour d'argent",
    "château de la tour de l": "château de la tour de l'ange",
    "château du domaine de l": "château du domaine de l'église",
    "château lagrange st julien": "château lagrange",
    "château la sauvageonne organic": "château la sauvageonne",
    "chosen by majestic greek": "chosen by majestic",
    "chosen by majestic grüner": "chosen by majestic",
    "cloudy bay te koko": "cloudy bay",
    "corallo nero d": "corallo",
    "croft 10 year old tawny port": "croft",
    "cune barrel fermented": "cvne",
    "cune": "cvne",  # Cune is CVNE's own name for its wines
    "de bortoli botrytis semillon": "de bortoli",
    "de forville barbera d": "de forville",
    "de forville dolcetto d": "de forville",
    "de forville langhe": "de forville",
    "definition albariño": "definition",
    "definition claret": "definition",
    "definition english": "definition",
    "definition grüner": "definition",
    "definition gsm": "definition",
    "definition hautescôtes": "definition",
    "definition mâconvillages": "definition",
    "devil": "devil's creek",
    "dom ruinart": "ruinart",
    "domaine andré et edmond figeat": "domaine figeat",
    "domaine cauvard choreylèsbeaune": "domaine cauvard",
    "domaine de la métairie d": "abbotts & delaunay",  # "Abbotts & Delaunay, Domaine de la Métairie d'Alon ..."
    "domaine des tourelles cuvée pierre brun": "domaine des tourelles",
    "domaine faiveley nuits saint georges": "faiveley",
    "domaine jomain": "jomain",
    "domaine jomain bourgogne côte d": "jomain",
    "jomain frères bourgogne": "jomain",  # "The Jomain family is known for its delicious Puligny-Montrachet"
    "domaine louis moreau petit": "domaine louis moreau",
    "domaine moillardthomas": "moillard-thomas",
    "moillardthomas": "moillard-thomas",
    "moillardthomas bourgogne": "moillard-thomas",
    "moillardthomas coteaux bourguignons": "moillard-thomas",
    "domaine pardon et fils": "pardon et fils",
    "domaine rolet arbois": "domaine rolet",
    "domaines ott château romassan": "domaines ott",
    "doudetnaudin bourgogne côte d": "doudet-naudin",
    "dr loosen slate hill": "dr loosen",
    "ernst loosen": "dr loosen",  # "Ernst Loosen's family have made fantastic Riesling on the Mosel"
    "duckhorn vineyards": "duckhorn",
    "errazuriz estate series": "errázuriz",
    "errazuriz max": "errázuriz",
    "errazuriz single vineyard": "errázuriz",
    "errazuriz wild ferment": "errázuriz",
    "viña errázuriz": "errázuriz",
    "falua tercius tinto": "falua",
    "feudi": "feudi di san gregorio",
    "fitou by mademoiselle jones": "katie jones",  # "Katie Jones is one of the UK's finest winemakers"
    "fonseca bin 27 port": "fonseca",
    "freixenet 00 alcohol free": "freixenet",
    "gérard bertrand clos d": "gérard bertrand",
    "girardin père et fils santenay": "girardin père et fils",
    "gonzalez byass solera cream sherry": "gonzalez byass",
    "tio pepe": "gonzalez byass",  # "Gonzalez Byass 'Tio Pepe' Fino Sherry"; the En Rama's copy names the Gonzalez family
    "hambledon classic cuvee": "hambledon",
    "harvey": "harvey's",
    "henriques and henriques 3 year old full rich madeira 50cl": "henriques & henriques",
    "herdade": "herdade de gambia",
    "hospices de beaujeu bourgogne": "hospices de beaujeu",
    "jaboulet": "paul jaboulet aîné",
    "jackson estate vintage widow": "jackson estate",
    "jean bon merlot igp pays d": "jean bon",
    "journey": "journey's end",
    "klein": "klein constantia",
    "krug grande cuvée": "krug",
    "la gioiosa ca divo spumante": "la gioiosa",
    "la marca extra dry": "la marca",
    "lanson le": "lanson",
    "lanson le black label": "lanson",
    "lanson le green label": "lanson",
    "lanson le vintage": "lanson",
    "laurentperrier": "laurent-perrier",
    "laurentperrier la cuvée": "laurent-perrier",
    "laurentperrier millésimé": "laurent-perrier",
    "le voyage d": "le voyage d'odette",
    "les hauts de castelmaure corbières": "les hauts de castelmaure",
    "les lauriers": "les lauriers du terroir",
    "les caveau du prieuré": "union des vignerons des côtes du rhône",  # its copy names the union
    "les frères lumière": "union des vignerons des côtes du rhône",  # its copy names the union
    "lfe 900 singlevineyard": "luis felipe edwards",
    "lópez de haro": "lopez de haro",
    "louis jadot beaujolaislantignié": "louis jadot",
    "louis jadot bourgogne pinot noir": "louis jadot",
    "louis latour bourgogne": "louis latour",
    "louis latour bourgogne côte d": "louis latour",
    "louis latour mâconlugny": "louis latour",
    "louis martini": "louis m martini",
    "louis pommery": "pommery",  # "Pommery is the first house to launch English fizz"
    "louis roederer cristal": "louis roederer",
    "louis roederer quartet": "louis roederer",
    "lulu l": "lulu",
    "léon perdigal côtesdurhône": "léon perdigal",
    "m chapoutier domaine des granges de mirabel": "m chapoutier",
    "mchapoutier": "m chapoutier",
    # "Selected by Majestic", the shop's value range
    "majestic crisp & zesty": "majestic",
    "majestic fizzy & fruity": "majestic",
    "majestic fizzy & juicy": "majestic",
    "majestic fresh & juicy": "majestic",
    "majestic loves": "majestic",
    "majestic mulled": "majestic",
    "majestic ripe & bold": "majestic",
    "majestic vibrant & fresh": "majestic",
    "marisco pride & glory": "marisco vineyards",
    "the ned": "marisco vineyards",  # "Brent founded his winery, Marisco Vineyards"
    "the ned noble": "marisco vineyards",
    "the king": "marisco vineyards",  # "Brent created the King Series"
    "martín códax albariño": "martín códax",
    "mas querido field blend": "mas querido",
    "meerlust rubicon": "meerlust",
    "men in": "men in white coats",
    "mendel selection": "mendel",
    "montes single vineyard": "montes",
    "morande": "morandé",
    "mud house chilean": "mud house",
    "negrar appassimento rosso": "cantina negrar",
    "nero oro appassimento": "nero oro",
    "oliver dubois": "olivier dubois",
    "orin swift palermo": "orin swift",
    "ornellaia": "tenuta dell'ornellaia",
    "tenuta dell": "tenuta dell'ornellaia",
    "oyster": "oyster bay",
    "parcel series saintestèphe": "parcel series",
    "pasqua dlz": "pasqua",
    "romeo & juliet": "pasqua",  # "Pasqua 'Romeo & Juliet' ..."
    "villa borghetti": "pasqua",  # "Pasqua 'Villa Borghetti' ..."
    "pedro": "pedro's almacenista selection",
    "marcelo pelleriti": "pelleriti",
    "penfolds bin 2 shirazmataro": "penfolds",
    "penfolds bin 8 shirazcabernet sauvignon": "penfolds",
    "penfolds bin a": "penfolds",
    "perdeberg wines the dry land collection": "perdeberg",
    "peter & ulrich griebeler dry": "peter & ulrich griebeler",
    "peter lehmann masters": "peter lehmann",
    "piperheidsieck": "piper-heidsieck",
    "pol roger pure extra": "pol roger",
    "pouillyfumé de ladoucette": "de ladoucette",
    "domaine de ladoucette": "de ladoucette",
    "primo rosso appassimento": "primo rosso",
    "remi seguin": "rémi seguin",
    "ridge east bench": "ridge",
    "ridge geyserville": "ridge",
    "rijckaert f rouve saint véran": "rijckaert f rouve",
    "roberto sarotto barbaresco riserva": "roberto sarotto",
    "royal tokaji 5 puttonyos": "royal tokaji",
    "royal tokaji late harvest": "royal tokaji",
    "rupert & rothschild baron edmond": "rupert & rothschild",
    "rutherglen shelley": "rutherglen shelley's block",
    "selborne classic cuvée": "selborne",
    "selladore en": "selladore",
    "springfield estate albariño": "springfield estate",
    "stag": "stag's leap",
    "taittinger comtes de": "taittinger",
    "taittinger prestige": "taittinger",
    "taylor": "taylor's",
    "taylors fine": "taylor's",
    "te mata estate syrah": "te mata estate",
    "ten minutes by tractor estate": "ten minutes by tractor",
    "the guv": "the guv'nor",
    "the hunting lodge seasonal": "the hunting lodge",
    "torbreck descendant": "torbreck",
    "trizanne signature wines": "trizanne",
    "two hands ares": "two hands",
    "tyrrell": "tyrrell's",
    "vallformosa fest": "vallformosa",
    "veuve clicquot demisec": "veuve clicquot",
    "veuve clicquot extra": "veuve clicquot",
    "vidalfleury": "vidal-fleury",
    "vik milla cala": "vik",
    "villa maria cellar selection": "villa maria",
    "villa tucci bianco": "villa tuccia",
    "villa tuccia rosso": "villa tuccia",
    "villiera barrel fermented": "villiera",
    "villiera cap classique": "villiera",
    "villiera wines": "villiera",
    "vinos barco mencía menciño": "vinos barco",
    "vinos del viento garnacha blanca": "vinos del viento",
    "viñalba malbecbonarda": "viñalba",
    "viñalba selección torrontés": "viñalba",
    "waimea estates albariño": "waimea estates",
    "waimea estates grüner": "waimea estates",
    "weingut wieninger gemischter satz": "weingut wieninger",
    "winemaker series the": "winemaker series",
    "winzer krems grüner": "winzer krems",
    "wolf blass yellow label": "wolf blass",
    "wynns coonawarra estate": "wynns",
    "yalumba cigar": "yalumba",
    "yalumba y series": "yalumba",
    "yealands estate single vineyard": "yealands",
    "canardduchêne": "canard-duchêne",
    "langloischateau": "langlois-chateau",
    "château caronne stegemme": "château caronne ste-gemme",
    "château grandpuylacoste": "château grand-puy-lacoste",
    "château lynchmoussas": "château lynch-moussas",
    "château rauzanségla": "château rauzan-ségla",
    "château tour hautcaussan": "château tour haut-caussan",
    "domaine hubert bouzereaugruère et filles": "domaine hubert bouzereau-gruère et filles",
    "domaine jeanmax roger": "domaine jean-max roger",
    "domaine le prieuré de saintcéols": "domaine le prieuré de saint-céols",
    "jeanlouis chavy": "jean-louis chavy",
    "jeanpierre bailly": "jean-pierre bailly",
    "lâchezvous grenachesyrah": "lâchez-vous",
}


def _producer_rule(row) -> str:
    """The words before the first quoted name; else before the grape, place, a style word or the vintage."""
    t = row["Title"].split(",")[0]
    m = re.split(r"['‘’\"“”]", t)
    if len(m) > 1 and m[0].strip():
        p = m[0]
    else:
        stops = set()
        for c in ["Grape", "Appellation", "Region", "Country"]:
            if isinstance(row[c], str):
                stops |= set(row[c].lower().split())
        toks = []
        for w in t.split():
            wl = w.lower().strip(".")
            if re.match(r"(19|20)\d\d", wl) or (toks and (wl in stops or wl in _STYLE_WORDS)):
                break
            toks.append(w)
        p = " ".join(toks) if toks else t
    return " ".join(re.sub(r"[^a-zà-ÿ0-9 &]", "", p.lower()).split())


def _producer_key(row) -> str:
    for start, producer in _PRODUCER_BY_TITLE_START.items():
        if row["Title"].startswith(start):
            return producer
    rough = _producer_rule(row)
    return _PRODUCER_MERGE.get(rough, rough)


class WineWorldCost(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What would a bottle of wine sell for in a UK wine shop, given its description?",
        use_case=(
            "For example, a producer or importer offering a wine to a UK merchant estimates the shelf price it would"
            " sell at, or a buyer judges whether a wine is good value against similar wines, from its catalogue entry"
            " and description."
        ),
        row=(
            "One wine sold by the bottle in a UK online wine shop, priced in pounds and scraped in 2023 (1,277 wines;"
            " most likely Majestic Wine, which 78 descriptions name)."
        ),
        predicted="The price of one bottle in pounds, on a log scale.",
        known=(
            "The wine's name and the shop's description, grapes, country, region and appellation, colour, style, "
            "tasting characteristics, closure, bottle size, alcohol content and vintage year."
        ),
        split=(
            "Wines of producers not seen in training, from the same shop and time: every wine of one producer is on "
            "one side, so the test wines stand for wines from a producer the shop does not list yet."
        ),
        changes=(
            "We added the producer, read from the title and checked by hand, as a group column and split by it; with "
            "random wines, 64% of the test wines had a wine of their producer in training."
        ),
        fit="approximate",
        fit_reason=(
            "The title and description are the shop's sales copy, written for wines it had already priced: they never "
            "state the price, but their wording follows the price tier. One unnamed shop (most likely Majestic Wine) "
            "at one time. The shop sets its prices from its costs, which the data do not hold; the model stands for "
            "someone who does not know the price."
        ),
    )

    # Dataset
    unique_name = "wine_world_cost"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/datasets/elvinrustam/wine-dataset",
            license="CC0: Public Domain",
            year="2023",
            bibtex=r"""
                @misc{Rustamov2023WineDataset,
                  author = {Elvin Rustamov},
                  title  = {Wine Dataset},
                  year   = {2023},
                  howpublished = {\url{https://www.kaggle.com/datasets/elvinrustam/wine-dataset}},
                  note   = {Kaggle dataset}
                }
            """,
        ),
    )
    download_description = """
        There are many different wine datasets available, but this one is a comprehensive collection of wine-related data that includes information on various wine characteristics and text. So we stick to it.

        kaggle datasets download elvinrustam/wine-dataset && unzip wine-dataset.zip && rm wine-dataset.zip
        mkdir -p local-data-warehouse/wine_world_cost && mv WineDataset.csv local-data-warehouse/wine_world_cost
    """
    curation_comments = """
        We start with the Kaggle version. We resolve several issues from the web scrapper.

        - We create a task to predict the price per bottle. We remove the 11 rows that have price information per case or each.
        - Create the price target by parsing the price column.
        - We map capacity to numeric values in ML.
        - We parse the ABV to a numeric value
        - We parse the vintage to a numeric date value, ensuring that each wine maps to the oldest year in its special syntax.
        - We log scale the target, as the price distribution is very skewed.
        - One description stated its wine's own earlier price: "Majestic Loves Rose 2019" (shelf price £6.99) opened
          with "Our mission was to find the best tasting wines at £5.99.", the range's earlier price. We remove that
          sentence from that one description (Andrej, 2026-11-10); the 13 other descriptions that name a price in
          pounds name other wines' prices, positioning copy that stays. Removing every sentence with price or value
          words changes R^2 by 0.003, so we keep the description (evidence in the record, 2026-10-14).
        - We drop the two spirits, rows with an ABV of 30% or more (Andrej, 2026-11-10): a 12-year-old single malt
          whisky (40%) and a tequila; the task prices a bottle of wine. The alcohol-free and fortified wines stay.
        - The shop's sales copy (title and description) is written for wines already priced and its wording follows
          the price tier (value wording at a median £13-15, critic and cru wording at £31-48), but it never states
          the price and adds about 0.09 R² over the tabular columns; it stays as part of the task, with an
          approximate fit (Andrej, 2026-11-10; as coffee_rating_prediction's review text).
        - The use case names someone who does not know the price (Andrej, 2026-11-11): a producer or importer
          estimating the UK shelf price of a wine it offers, or a buyer judging value. The shop itself prices from its
          costs (supplier price, duty, VAT, margin), which the data do not hold; the shop's copy stands in for the
          producer's own tasting note.
        - Grouped by producer since 2026-11-11 (random before; Andrej, 2026-11-11): the closest real use the data can test
          is pricing a wine from a producer the shop does not list yet. The data hold no listing date, so no
          split forward in time can be built; under the random split 64% of the test wines had a wine of the same
          producer in training. RMSLE, 3 folds (3 repeats for TabPFN, 10 for the others), random against grouped by
          this producer key: TabPFN-3.5 0.345 / 0.375, LightGBM 0.383 / 0.410, ridge on TF-IDF 0.365 / 0.403; every
          model loses 0.03 to 0.04 and TabPFN stays ahead.
        - The producer key (`Producer`, the group column, no feature): the data have no producer column. A rule reads it
          from the title (the words before the first quoted name; else before the grape, place, a style word or the
          vintage), and two tables fix what the rule gets wrong: titles that start with an appellation, a second wine or
          a brand (47 rows), and spelling variants, name forms, ranges and brands of one producer (339 rows). All 1,277
          titles were checked by hand (2026-11-11). One producer is the house, estate, winery or cooperative that makes
          and sells the wine under its name; its brands, ranges and second wines join it when the title or the shop's
          copy names it as their maker (Tio Pepe with Gonzalez Byass, The Ned and The King's series with Marisco
          Vineyards, Armand de Brignac with Cattier, Amiral de Beychevelle with Château Beychevelle). Estates with their
          own name stay apart from the group that owns them (Château Lynch-Moussas and Château Batailley, Domaine de
          Villemajou and Gérard Bertrand), and corporate owners are not merged (Dom Pérignon and Moët & Chandon,
          Alamos and Catena). The shop's own-label ranges are one group each, although some of their copy names the
          maker (Definition Fleurie by Pardon et Fils): the shop prices the range, and the maker is not named for all.
          613 producers, 1 to 35 wines (Definition), 250 with more than one wine.
        - Time basis: Snapshot: one scrape of a UK online wine shop's range (most likely Majestic Wine) in 2023; the
          shelf prices, sales copy and catalogue attributes of that moment; the vintage is a wine attribute, not a
          time. Not tested: prices after 2023.
    """

    # Task
    target = "Price"
    problem_type = "regression"
    metric = Metric.from_context(
        "rmsle",
        reason="A scraped Kaggle dataset with no competition, paper or stated metric. For a bottle's price the error that matters is relative to the price (a pound off a cheap bottle is a large miss, on a rare one a small one), so RMSLE on the price.",
        target_transform="log",
    )

    grouping = Grouping(
        on="Producer",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a producer: the house, estate, winery or cooperative that makes and sells the wine under its name, with its brands, ranges and second wines (613 producers, 1 to 35 wines; 250 with more than one). The data have no producer column; the key is read from the title and checked by hand (curation comments). The use case is a producer, importer or buyer estimating the shelf price of a wine not on the list, often from a producer the shop does not sell yet; such a wine has no sibling in the price list to read the price level from, so the test producers are new to the model. The shop's own-label ranges (Definition, Chosen by Majestic, Selected by Majestic, Parcel Series, Winemaker Series) are one group each. Each row is one prediction, made from the wine's catalogue entry and the shop's copy.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the producer: all wines of one producer stay on one side, so a model prices wines from producers it has not seen, from the same shop and time. Wines of the same region, grape or style are on both sides.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "WineDataset.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df[df["Per bottle / case / each"] == "per bottle"].reset_index(drop=True)
        df["Price"] = df["Price"].apply(lambda x: x.replace("£", "").replace(" per bottle", "")).astype(float)
        df["ABV%"] = df["ABV"].apply(lambda x: str(x).replace("ABV ", "").replace("%", "")).astype(float)
        # Two spirits (a whisky and a tequila) are not wine
        df = df[~(df["ABV%"] >= 30)].reset_index(drop=True)
        # One description quotes its own wine's earlier price
        stated_price = "Our mission was to find the best tasting wines at £5.99."
        has_price = df["Description"].fillna("").str.contains(stated_price, regex=False)
        assert has_price.sum() == 1
        assert df.loc[has_price, "Title"].iloc[0] == "Majestic Loves Rose 2019"
        df.loc[has_price, "Description"] = (
            df.loc[has_price, "Description"].str.replace(stated_price, "", regex=False).str.strip()
        )
        # The producer, the group of the split (no feature)
        df["Producer"] = df.apply(_producer_key, axis=1)
        assert df["Producer"].nunique() == 613
        df["Capacity"] = (
            df["Capacity"]
            .map(
                {
                    "75CL": 750,
                    "37.5CL": 375,
                    "1.5LTR": 1500,
                    "750ML": 750,
                    "150CL": 1500,
                    "50CL": 500,
                    "70CL": 700,
                    "500ML": 500,
                    "375ML": 375,
                    "300CL": 3000,
                }
            )
            .astype(float)
        )
        df["VintageYear"] = pd.to_datetime(df["Vintage"].apply(lambda x: x.split("/")[0]).replace("NV", np.nan)).dt.year
        df = df.drop(
            columns=[
                # Constant
                "Per bottle / case / each",
                # Meaning of feature is missing, and it is unclear how to interpret it
                "Unit",
                # Copied columns
                "ABV",
                "Vintage",
            ]
        )
        # Log scale target
        df["Price"] = np.log(df["Price"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "Producer",
                "Closure",
                "Type",
                "Style",
            ],
            string=[
                "Title",
                "Description",
                "Grape",
                "Secondary Grape Varieties",
                "Country",
                "Characteristics",
                "Region",
                "Appellation",
            ],
        )
