#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventaire exhaustif des attributs DATES du graphe GRC-20 — LECTURE SEULE.

POURQUOI CE SCRIPT EXISTE. Le graphe porte 948 valeurs datees reparties sur
24 cles d'attribut et six familles de format incompatibles : des horodatages
ISO-Z (« 2016-04-30T00:00:00.000Z »), des dates ISO tronquees (« 2010-06 »),
des annees nues (« 2013 »), des dates a barres obliques dont l'ordre
jour/mois n'est pas declare (« 01/04/2014 »), des plages (« 2015-2017 ») et
du texte libre (« fin 2013 — pression FinCEN »). Aucun inventaire ne disait
jusqu'ici combien il y en a, ni lesquelles sont indecidables. Ce script
MESURE. Il ne repare rien, ne tranche rien, et ne devine aucun jour.

CE QU'IL N'ECRIT JAMAIS : le graphe, aucune carte d'ancrage, aucun patch,
aucun HTML. Sa seule ecriture possible est le CSV d'inventaire, et seulement
quand `--csv` est passe. Sans `--csv`, il est integralement en lecture seule.

=====================================================================
LE PERIMETRE — 24 cles, et pourquoi `page_start` n'en fait PAS partie
=====================================================================
Les 24 cles de `CLES_DATEES` ont ete relevees empiriquement dans v111, pas
devinees par une regex sur les noms. C'est important, parce qu'une regex
naive sur « start » / « date » / « year » ramasse `page_start`, qui n'est
PAS une date : c'est le numero de la PAGE IMPRIMEE ou commence une section
de la these (37 noeuds ; cf. `scripts/audit_section_page_start.py`, qui
l'audite contre les PDF canoniques). La confondre avec une date produirait
37 lignes « annee 202 hors plage » qui ne veulent rien dire. Elle est donc
exclue explicitement, par une constante nommee, et non par omission.

DEUX DES 24 CLES NE PORTENT PAS DE DATE, et le CSV le dit plutot que de le
masquer : `dateSource` (95 valeurs) porte une REFERENCE BIBLIOGRAPHIQUE
(« Sedgwick 2018e », « Banque de France 2013, p. 4 ») et `dateAuthority`
(49 valeurs) un NIVEAU DE PREUVE (`AUTHOR_VERIFIED`, `EXTERNAL_VERIFICATION`,
`TIMELINE_FIGURE`). Elles disent d'ou vient une date, pas quand. Elles
figurent dans l'inventaire parce que le perimetre demande les couvre, avec
`plausibility_flag=non_parsable` et une note qui nomme leur nature. Les
retirer en silence aurait fabrique un inventaire qui ne correspond plus a
son perimetre declare.

DES CLES DATEES RESTENT HORS PERIMETRE, et le rapport les nomme. `founded`,
`launch`, `created`, `publicDisclosure`, `firstPublication`, `formalized`,
`introduced`, `closed`, `launched`, `released`, `dissolved`, `active`,
`firstContactCM` portent elles aussi des dates, sous d'autres noms. Le bloc
« VEILLE » de stdout les liste avec un decompte, par une heuristique
DECLAREE (une valeur courte contenant une annee de 1500 a 2049), pour que
l'auteur decide si le perimetre doit s'elargir. Elles n'entrent pas dans le
CSV : un inventaire dont le perimetre bouge tout seul n'est plus une preuve.

=====================================================================
LA REGLE DE NORMALISATION — deux niveaux, jamais de devinette
=====================================================================
NIVEAU 1 (remplit `normalized_iso`) : la valeur, une fois les espaces
reduits, correspond ENTIEREMENT a une forme reconnue. Egalite de forme, pas
approximation :
    TIME-ISO-Z                « 2016-04-30T00:00:00.000Z »  -> jour
    ISO-jour                  « 2010-07-15 »                -> jour
    ISO-mois                  « 2010-06 »                   -> mois
    annee                     « 2013 », NUMBER 2010         -> annee
    DD-MM-YYYY-ou-MM-DD-YYYY  « 15/08/2010 »                -> jour
    plage-annees              « 2015-2017 », « 2013- »      -> plage
    libre, sous-forme datee   « 25 decembre 2018 », « Mars 2013 »
    libre, plage a 2 bornes   « 18/07/2008 — 31/03/2012 »   -> plage
La colonne `format_family` s'en tient a la nomenclature demandee : une date
en toutes lettres et une plage a deux bornes datees y tombent donc dans
`libre`, bien qu'elles soient entierement derivables. `granularity` et
`normalized_iso` disent la difference, et stdout detaille `libre` par
sous-forme pour qu'on ne lise pas 222 « textes opaques » la ou il y en a 158.
Pour toute PLAGE, `normalized_iso` reste VIDE : retenir une des deux bornes
comme « la » date serait un arbitrage.
La date est en plus verifiee comme date de CALENDRIER (le 31/02 serait
`non_parsable`, pas normalise).

NIVEAU 2 : tout le reste. `normalized_iso` reste VIDE. Le script ne fait
AUCUNE extraction opportuniste d'annee dans une valeur libre — parce que
« Sedgwick 2018e » contient « 2018 » sans etre date de quoi que ce soit, et
que « fin 2013 — pression FinCEN » designe une fin de periode que seul
l'auteur peut borner. Les annees reperees dans ces valeurs sont reportees
dans `notes` sous le marqueur « ANNEES CITEES », jamais promues en donnee.

L'AMBIGUITE JOUR/MOIS N'EST JAMAIS TRANCHEE. « 15/08/2010 » est decidable
(15 ne peut pas etre un mois) : normalise en 2010-08-15. « 01/04/2014 » ne
l'est pas : `dmy_ambiguous=oui`, `normalized_iso` s'ARRETE A L'ANNEE
(« 2014 ») et `granularity` reste `jour` — la valeur a bien la precision du
jour, c'est son identite qui est indecidable. Aucune heuristique (« le
depot est francais, donc DD/MM ») n'est appliquee : ce serait un arbitrage
deguise en normalisation.

=====================================================================
LES CONFLITS — des SIGNALEMENTS, jamais des verdicts
=====================================================================
`intra_entity_conflict` ne compare que des cles de MEME ROLE, parce que
comparer des roles differents fabrique des faux positifs evidents :
    point       year date dateEvenement dateInterview launchYear
                foundedYear dateDefense fork_date dateIntroduced
    debut       dateDebut dateStart timeStart startDateText
    fin         dateEnd timeEnd endDateText closedYear regulatoryEnd
    plage       period dateRange coveragePeriod
    provenance  dateSource dateAuthority consultedDate
Sans cette partition, la these (`dateStart` 2018, `dateDefense` 2024) et
MtGox (`foundedYear` 2010, `closedYear` 2014) seraient signales alors qu'ils
sont exacts, et un lecteur presse aurait « corrige » une donnee juste.
Les divergences INTER-ROLE existantes ne sont pas perdues pour autant : elles
vont dans `notes` sous « ECART INTER-ROLE (non-verdict) », avec les deux
valeurs nommees. `notes` dit toujours QUOI est compare a QUOI.

`description_conflict` compare l'ANNEE de `normalized_iso` aux annees
extraites de la `description` de la meme entite. Une description est de la
prose : elle cite volontiers des annees qui ne sont pas la date de l'entite
(« Tasca & Liu 2018 » dans une phase 2012-2013). Un desaccord est donc une
piste de lecture, pas une erreur etablie — d'ou le champ `notes` qui donne
les deux cotes.

=====================================================================
LA PLAUSIBILITE — precedence STRICTE, dans cet ordre
=====================================================================
  1. `non_parsable`  aucune annee n'a pu etre derivee du niveau 1.
  2. `annee_hors_plage`  une annee < 1400 ou > 2030 (la these court des
     origines des CM a 2020 ; hors de ces bornes, c'est une faute de
     saisie, pas une date).
  3. `futur`  la date est posterieure a DATE_REFERENCE. Cette date est une
     CONSTANTE GELEE (2026-08-08, jour de l'inventaire) et non
     `date.today()` : un CSV dont le contenu change avec l'horloge ne peut
     pas etre compare par `--check`. `--aujourdhui` permet de la rejouer
     autrement, en connaissance de cause.
  4. `anterieure_a_2008_sur_entite_crypto`  l'entite est de type Protocol,
     InfrastructureEvent, CrisisEvent, ProtocolChange, ProtocolProposal,
     SmartContract ou SoftwareClient, et la date precede le 31/10/2008
     (publication du livre blanc Bitcoin). Une granularite trop grossiere
     pour trancher (annee 2008 seule) n'est PAS signalee : la note le dit.
  5. `ok`
Une valeur peut relever de plusieurs cases (l'an 3000 est futur ET hors
plage) : le drapeau retenu est le premier de la liste, et `notes` mentionne
les autres. Aucune information n'est perdue par la precedence.

DETERMINISME. Tri par (`entity_id`, `attribute_key`), aucun horodatage dans
la sortie, aucun parcours d'ensemble non trie : deux executions rendent un
CSV identique octet pour octet. C'est ce que `--check` verifie.

CODES DE SORTIE : 0 = l'inventaire a tourne (des `non_parsable` et des
conflits sont un RESULTAT, pas une panne) ; 1 = `--check` a trouve une
divergence entre le CSV verse et le CSV regenere ; 2 = erreur d'invocation.

Usage:
    python3 scripts/audit_chronology_dates.py
    python3 scripts/audit_chronology_dates.py --csv
    python3 scripts/audit_chronology_dates.py --csv /tmp/inventaire.csv
    python3 scripts/audit_chronology_dates.py --check
"""
import argparse
import collections
import csv
import datetime
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import (REPO, graphe_le_plus_recent,  # noqa: E402
                          numero_de_version, sans_accents)

CODE_DIVERGENCE = 1
CODE_INVOCATION = 2

CSV_AUTO = '<auto>'   # sentinelle : nom derive de la version du graphe

# ---------------------------------------------------------------------------
# PERIMETRE
# ---------------------------------------------------------------------------
# Les 24 cles relevees dans v111. L'ordre est celui de l'effectif decroissant
# constate — il ne sert qu'a l'affichage, le CSV est trie par (id, cle).
CLES_DATEES = (
    'year', 'date', 'dateSource', 'dateAuthority', 'dateInterview',
    'dateEvenement', 'consultedDate', 'period', 'launchYear', 'dateDebut',
    'timeStart', 'timeEnd', 'dateStart', 'foundedYear', 'dateEnd',
    'dateRange', 'startDateText', 'endDateText', 'closedYear', 'dateDefense',
    'coveragePeriod', 'fork_date', 'dateIntroduced', 'regulatoryEnd',
)

# EXCLUSION EXPLICITE, cf. docstring : `page_start` matche une regex naive sur
# « start » mais porte un numero de PAGE IMPRIMEE de la these, pas une date.
# Elle est nommee ici pour que l'exclusion soit lisible et testable, et non
# obtenue par le silence d'une liste.
CLES_EXCLUES_NON_DATEES = ('page_start',)

# Cles qui documentent la PROVENANCE d'une date sans en etre une. Elles
# restent dans l'inventaire (le perimetre les demande) mais ne peuvent pas
# etre normalisees, et le rapport les compte a part.
CLES_NON_DATEES_DANS_LE_PERIMETRE = {
    'dateSource': "reference bibliographique de la date (ex. « Sedgwick "
                  "2018e »), pas une date",
    'dateAuthority': "niveau de preuve de la date (AUTHOR_VERIFIED / "
                     "EXTERNAL_VERIFICATION / TIMELINE_FIGURE), pas une date",
}

ROLES = {
    'point': ('year', 'date', 'dateEvenement', 'dateInterview', 'launchYear',
              'foundedYear', 'dateDefense', 'fork_date', 'dateIntroduced'),
    'debut': ('dateDebut', 'dateStart', 'timeStart', 'startDateText'),
    'fin': ('dateEnd', 'timeEnd', 'endDateText', 'closedYear',
            'regulatoryEnd'),
    'plage': ('period', 'dateRange', 'coveragePeriod'),
    'provenance': ('dateSource', 'dateAuthority', 'consultedDate'),
}
ROLE_DE_CLE = {cle: role for role, cles in ROLES.items() for cle in cles}
# Seuls ces roles se comparent a eux-memes (cf. docstring).
ROLES_COMPARABLES = ('point', 'debut', 'fin')

TYPES_CRYPTO = ('Protocol', 'InfrastructureEvent', 'CrisisEvent',
                'ProtocolChange', 'ProtocolProposal', 'SmartContract',
                'SoftwareClient')

# Constante GELEE — cf. docstring, section PLAUSIBILITE.
DATE_REFERENCE = datetime.date(2026, 8, 8)
SEUIL_CRYPTO = datetime.date(2008, 10, 31)   # livre blanc Bitcoin
ANNEE_MIN = 1400
ANNEE_MAX = 2030

COLONNES = (
    'entity_id', 'entity_name', 'entity_types', 'attribute_key',
    'grc20_value_type', 'raw_value', 'normalized_iso', 'granularity',
    'format_family', 'dmy_ambiguous', 'type_key_mismatch',
    'intra_entity_conflict', 'description_date_hint', 'description_conflict',
    'plausibility_flag', 'notes',
)

FAMILLES = ('TIME-ISO-Z', 'ISO-jour', 'ISO-mois', 'annee',
            'DD-MM-YYYY-ou-MM-DD-YYYY', 'plage-annees', 'libre')
GRANULARITES = ('jour', 'mois', 'annee', 'plage', 'indeterminee')
PLAUSIBILITES = ('ok', 'futur', 'anterieure_a_2008_sur_entite_crypto',
                 'annee_hors_plage', 'non_parsable')

# ---------------------------------------------------------------------------
# mois : le niveau 1 n'accepte que les formes PLEINES (pas les abreviations),
# la detection dans les descriptions accepte en plus les abreviations usuelles.
# ---------------------------------------------------------------------------
MOIS_PLEINS = {
    'janvier': 1, 'fevrier': 2, 'mars': 3, 'avril': 4, 'mai': 5, 'juin': 6,
    'juillet': 7, 'aout': 8, 'septembre': 9, 'octobre': 10, 'novembre': 11,
    'decembre': 12,
    'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
    'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11,
    'december': 12,
}
MOIS_ABREGES = {
    'janv': 1, 'fev': 2, 'avr': 4, 'juil': 7, 'sept': 9, 'oct': 10,
    'nov': 11, 'dec': 12,
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6, 'jul': 7, 'aug': 8,
    'sep': 9,
}
MOIS_TOUS = dict(MOIS_ABREGES)
MOIS_TOUS.update(MOIS_PLEINS)          # les formes pleines priment

# formes reconnues au niveau 1
RE_ISO_Z = re.compile(
    r'^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?Z$')
RE_ISO_JOUR = re.compile(r'^(\d{4})-(\d{2})-(\d{2})$')
RE_ISO_MOIS = re.compile(r'^(\d{4})-(\d{2})$')
RE_ANNEE = re.compile(r'^(\d{4})$')
RE_BARRES = re.compile(r'^(\d{1,2})[/.](\d{1,2})[/.](\d{4})$')
RE_PLAGE = re.compile(r'^(\d{4})\s*[-–—]\s*(\d{4})$')
RE_PLAGE_OUVERTE = re.compile(r'^(\d{4})\s*[-–—]\s*$')
# Plage dont les DEUX bornes sont des dates completes : « 18/07/2008 —
# 31/03/2012 », « avril 2012 – octobre 2013 ». Le separateur exige un tiret
# cadratin/demi-cadratin, ou un trait d'union ENTOURE D'ESPACES : sans cette
# contrainte, « 2010-06 » (ISO-mois) serait coupe en deux.
RE_SEPARATEUR_PLAGE = re.compile(r'\s+[–—]\s+|\s+-\s+|[–—]')
_MOIS_ALT = '|'.join(sorted(MOIS_PLEINS, key=len, reverse=True))
RE_TEXTE_JOUR = re.compile(
    r'^(?:le\s+)?(\d{1,2})(?:er)?\s+(' + _MOIS_ALT + r')\s+(\d{4})$')
RE_TEXTE_MOIS = re.compile(r'^(' + _MOIS_ALT + r')\s+(\d{4})$')

# annees isolees, pour les notes « ANNEES CITEES » et les descriptions
RE_ANNEE_LIBRE = re.compile(r'(?<!\d)(\d{4})(?!\d)')
_MOIS_TOUS_ALT = '|'.join(sorted(MOIS_TOUS, key=len, reverse=True))
RE_MOIS_ANNEE = re.compile(
    r'\b(' + _MOIS_TOUS_ALT + r')\.?\s+(?:de\s+|of\s+)?(\d{4})\b')

# VEILLE : ce qui, hors perimetre, ressemble a une date. Heuristique
# DECLAREE (cf. docstring) — elle n'alimente que stdout, jamais le CSV.
RE_VEILLE = re.compile(r'(?<!\d)(1[5-9]\d\d|20[0-4]\d)(?!\d)')
VEILLE_LONGUEUR_MAX = 60


# --------------------------------------------------------------------------
# invocation
# --------------------------------------------------------------------------
def echec_invocation(msg):
    print(f"ECHEC (invocation) : {msg}", file=sys.stderr)
    sys.exit(CODE_INVOCATION)


def lire_json(chemin, quoi):
    if not chemin or not os.path.exists(chemin):
        echec_invocation(f"{quoi} introuvable : {chemin}")
    try:
        with open(chemin, encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as err:
        echec_invocation(f"{quoi} illisible : {err}")


def csv_defaut(chemin_graphe):
    """Nom du CSV derive de la VERSION du graphe inventorie.

    Fige sur v111, le chemin par defaut aurait reecrit la preuve v111 avec
    des donnees v112 des qu'un graphe plus recent existe."""
    version = numero_de_version(chemin_graphe or '')
    suffixe = f"v{version}" if version is not None else 'vX'
    return os.path.join(REPO, 'docs', 'audits', 'data',
                        f'chronology-date-inventory-{suffixe}.csv')


# --------------------------------------------------------------------------
# normalisation
# --------------------------------------------------------------------------
def plie(texte):
    """Minuscules, sans accents, espaces reduits. Ne supprime rien d'autre."""
    return ' '.join(sans_accents(str(texte or '')).lower().split())


def valeur_brute(attribut):
    """La valeur d'un attribut GRC-20, qu'il soit {type, value} ou brut."""
    if isinstance(attribut, dict):
        return attribut.get('value')
    return attribut


def type_grc20(attribut):
    """Le type DECLARE de l'attribut ; 'RAW' quand l'attribut n'est pas un dict."""
    if isinstance(attribut, dict):
        return str(attribut.get('type') or '')
    return 'RAW'


def date_valide(annee, mois, jour):
    try:
        return datetime.date(annee, mois, jour)
    except ValueError:
        return None


class Lecture:
    """Ce que le niveau 1 a pu etablir d'une valeur. Aucun champ n'est devine."""

    def __init__(self):
        self.iso = ''             # normalized_iso
        self.granularite = 'indeterminee'
        self.famille = 'libre'
        self.dmy = ''             # '', 'oui', 'non'
        self.annees = []          # annees ETABLIES (triees) : 0, 1 ou 2
        self.borne_min = None     # date la plus precoce etablie, si connue
        # Les DEUX dates possibles quand l'ordre jour/mois est indecidable.
        # Vide sinon. Sert a ne pas juger une valeur ambigue sur une seule de
        # ses lectures : voir la sortie `anterieure_a_2008_sur_entite_crypto`.
        self.lectures_possibles = []
        self.notes = []


def analyse(cle, type_declare, brute, plages=True):
    """-> Lecture. Niveau 1 uniquement : une forme reconnue, ou rien.

    `plages=False` interdit la reconnaissance d'une plage a deux bornes : ce
    mode sert a lire CHAQUE borne d'une plage sans risque de recursion.
    """
    lu = Lecture()
    if brute is None:
        lu.notes.append("valeur absente (cle presente sans valeur)")
        return lu

    # NUMBER : un entier a quatre chiffres est une annee ; tout autre nombre
    # ne l'est pas, et on ne le force pas.
    if isinstance(brute, bool):
        lu.notes.append("valeur booleenne : aucune date derivable")
        return lu
    if isinstance(brute, int) or isinstance(brute, float):
        if isinstance(brute, float) and not brute.is_integer():
            lu.notes.append("valeur numerique non entiere : aucune date "
                            "derivable")
            return lu
        entier = int(brute)
        if 1000 <= entier <= 9999:
            lu.famille, lu.granularite = 'annee', 'annee'
            lu.iso = f"{entier:04d}"
            lu.annees = [entier]
            lu.borne_min = datetime.date(entier, 1, 1)
            return lu
        lu.notes.append(f"valeur numerique {entier} : hors forme d'annee a "
                        "quatre chiffres, aucune date derivable")
        return lu

    texte = ' '.join(str(brute).split())
    if not texte:
        lu.notes.append("valeur vide")
        return lu

    m = RE_ISO_Z.match(texte)
    if m:
        annee, mois, jour = int(m.group(1)), int(m.group(2)), int(m.group(3))
        reelle = date_valide(annee, mois, jour)
        if reelle is None:
            lu.notes.append(f"horodatage ISO-Z non valide au calendrier : "
                            f"{texte}")
            return lu
        lu.famille, lu.granularite = 'TIME-ISO-Z', 'jour'
        lu.iso = reelle.isoformat()
        lu.annees = [annee]
        lu.borne_min = reelle
        if m.group(4) != '00' or m.group(5) != '00' or m.group(6) != '00':
            lu.notes.append("horodatage avec une heure non nulle : "
                            f"{m.group(4)}:{m.group(5)}:{m.group(6)} UTC")
        if cle == 'year' and (mois, jour) == (1, 1):
            lu.notes.append("cle `year` encodee en TIME au 1er janvier : la "
                            "precision jour est un artefact d'encodage, la "
                            "donnee utile est l'annee")
        elif cle == 'year':
            lu.notes.append("cle `year` mais horodatage a une date precise "
                            f"({reelle.isoformat()}), pas au 1er janvier")
        if type_declare not in ('TIME', ''):
            lu.notes.append(f"forme ISO-Z portee par un attribut declare "
                            f"{type_declare}")
        return lu

    m = RE_ISO_JOUR.match(texte)
    if m:
        annee, mois, jour = int(m.group(1)), int(m.group(2)), int(m.group(3))
        reelle = date_valide(annee, mois, jour)
        if reelle is None:
            lu.notes.append(f"date ISO non valide au calendrier : {texte}")
            return lu
        lu.famille, lu.granularite = 'ISO-jour', 'jour'
        lu.iso = reelle.isoformat()
        lu.annees = [annee]
        lu.borne_min = reelle
        return lu

    m = RE_ISO_MOIS.match(texte)
    if m:
        annee, mois = int(m.group(1)), int(m.group(2))
        if not 1 <= mois <= 12:
            lu.notes.append(f"mois hors 01-12 : {texte}")
            return lu
        lu.famille, lu.granularite = 'ISO-mois', 'mois'
        lu.iso = f"{annee:04d}-{mois:02d}"
        lu.annees = [annee]
        lu.borne_min = datetime.date(annee, mois, 1)
        return lu

    m = RE_ANNEE.match(texte)
    if m:
        annee = int(m.group(1))
        lu.famille, lu.granularite = 'annee', 'annee'
        lu.iso = f"{annee:04d}"
        lu.annees = [annee]
        lu.borne_min = datetime.date(annee, 1, 1)
        return lu

    m = RE_BARRES.match(texte)
    if m:
        a, b, annee = int(m.group(1)), int(m.group(2)), int(m.group(3))
        lu.famille, lu.granularite = 'DD-MM-YYYY-ou-MM-DD-YYYY', 'jour'
        lu.annees = [annee]
        lu.borne_min = datetime.date(annee, 1, 1)
        if a <= 12 and b <= 12:
            lu.dmy = 'oui'
            lu.iso = f"{annee:04d}"
            # Les deux lectures sont de vraies dates ; la plus precoce des
            # deux est une borne inferieure ETABLIE, la ou le 1er janvier
            # n'etait qu'un defaut de famille. La distinction compte pour le
            # seuil crypto : « 01/12/2008 » se lit 12 janvier OU 1er decembre,
            # de part et d'autre du 31/10/2008.
            lu.lectures_possibles = sorted({datetime.date(annee, b, a),
                                            datetime.date(annee, a, b)})
            lu.borne_min = lu.lectures_possibles[0]
            if a == b:
                lu.notes.append(
                    f"ordre jour/mois indecidable ({a:02d}/{b:02d}) mais les "
                    "deux groupes sont egaux : les deux lectures donnent la "
                    f"meme date {annee:04d}-{a:02d}-{b:02d} — normalized_iso "
                    "s'arrete tout de meme a l'annee, aucune lecture n'etant "
                    "etablie")
            else:
                lu.notes.append(
                    f"ordre jour/mois indecidable : « {texte} » se lit "
                    f"{annee:04d}-{b:02d}-{a:02d} (JJ/MM) ou "
                    f"{annee:04d}-{a:02d}-{b:02d} (MM/JJ) ; normalized_iso "
                    "s'arrete a l'annee, aucune convention n'est appliquee")
            return lu
        lu.dmy = 'non'
        if a > 12 and b <= 12:
            jour, mois, ordre = a, b, 'JJ/MM/AAAA'
        elif b > 12 and a <= 12:
            jour, mois, ordre = b, a, 'MM/JJ/AAAA'
        else:
            lu.notes.append(f"les deux groupes depassent 12 : « {texte} » "
                            "n'est ni JJ/MM ni MM/JJ")
            lu.granularite = 'indeterminee'
            lu.annees = []
            lu.borne_min = None
            lu.dmy = 'non'
            return lu
        reelle = date_valide(annee, mois, jour)
        if reelle is None:
            lu.notes.append(f"date a barres non valide au calendrier : {texte}")
            lu.granularite = 'indeterminee'
            lu.annees = []
            lu.borne_min = None
            return lu
        lu.iso = reelle.isoformat()
        lu.borne_min = reelle
        lu.notes.append(f"ordre etabli sans convention : le groupe {a if a > 12 else b} "
                        f"depasse 12 et ne peut pas etre un mois ({ordre})")
        return lu

    m = RE_PLAGE.match(texte) if plages else None
    if m:
        debut, fin = int(m.group(1)), int(m.group(2))
        lu.famille, lu.granularite = 'plage-annees', 'plage'
        lu.annees = sorted({debut, fin})
        lu.borne_min = datetime.date(min(debut, fin), 1, 1)
        lu.notes.append(f"plage d'annees {debut}-{fin} : normalized_iso reste "
                        "vide, choisir une des deux bornes serait un arbitrage")
        if fin < debut:
            lu.notes.append("borne finale ANTERIEURE a la borne initiale")
        return lu

    m = RE_PLAGE_OUVERTE.match(texte) if plages else None
    if m:
        debut = int(m.group(1))
        lu.famille, lu.granularite = 'plage-annees', 'plage'
        lu.annees = [debut]
        lu.borne_min = datetime.date(debut, 1, 1)
        lu.notes.append(f"plage ouverte a droite (« {texte} ») : debut {debut}, "
                        "fin non declaree")
        return lu

    # Plage a deux bornes datees, chacune relue au niveau 1. Sans ce cas,
    # « 18/07/2008 — 31/03/2012 » serait declare non parsable alors que ses
    # deux bornes sont parfaitement lisibles — et l'inventaire aurait
    # exagere son propre taux d'illisible.
    if plages:
        morceaux = [m.strip() for m in RE_SEPARATEUR_PLAGE.split(texte)]
        if len(morceaux) == 2 and all(morceaux):
            gauche = analyse(cle, type_declare, morceaux[0], plages=False)
            droite = analyse(cle, type_declare, morceaux[1], plages=False)
            if gauche.annees and droite.annees:
                lu.granularite = 'plage'
                lu.annees = sorted({gauche.annees[0], droite.annees[0]})
                lu.borne_min = min(b for b in (gauche.borne_min,
                                               droite.borne_min)
                                   if b is not None)
                if 'oui' in (gauche.dmy, droite.dmy):
                    lu.dmy = 'oui'
                lu.notes.append(
                    "plage a deux bornes datees : « "
                    f"{morceaux[0]} » -> {gauche.iso or gauche.annees[0]} et "
                    f"« {morceaux[1]} » -> {droite.iso or droite.annees[0]} ; "
                    "famille `libre` par convention de colonne (la "
                    "nomenclature ne prevoit que `plage-annees`), "
                    "normalized_iso reste vide, choisir une borne serait un "
                    "arbitrage")
                if lu.dmy == 'oui':
                    lu.notes.append(
                        "au moins une borne a un ordre jour/mois indecidable "
                        "— l'annee de chaque borne reste, elle, etablie")
                if droite.borne_min is not None and gauche.borne_min is not None \
                        and droite.borne_min < gauche.borne_min:
                    lu.notes.append("borne finale ANTERIEURE a la borne "
                                    "initiale")
                return lu

    # sous-formes datees du texte libre (famille `libre`, cf. docstring)
    aplati = plie(texte)
    m = RE_TEXTE_JOUR.match(aplati)
    if m:
        jour, annee = int(m.group(1)), int(m.group(3))
        mois = MOIS_PLEINS[m.group(2)]
        reelle = date_valide(annee, mois, jour)
        if reelle is None:
            lu.notes.append(f"date en toutes lettres non valide au "
                            f"calendrier : {texte}")
            return lu
        lu.granularite = 'jour'
        lu.iso = reelle.isoformat()
        lu.annees = [annee]
        lu.borne_min = reelle
        lu.notes.append("date en toutes lettres (jour, mois, annee) : famille "
                        "`libre` par convention de colonne, mais entierement "
                        "derivable")
        return lu
    m = RE_TEXTE_MOIS.match(aplati)
    if m:
        annee = int(m.group(2))
        mois = MOIS_PLEINS[m.group(1)]
        lu.granularite = 'mois'
        lu.iso = f"{annee:04d}-{mois:02d}"
        lu.annees = [annee]
        lu.borne_min = datetime.date(annee, mois, 1)
        lu.notes.append("mois en toutes lettres + annee : famille `libre` par "
                        "convention de colonne, mais entierement derivable")
        return lu

    # niveau 2 : rien n'est derive, les annees citees sont seulement signalees
    citees = sorted({int(a) for a in RE_ANNEE_LIBRE.findall(texte)})
    if citees:
        lu.notes.append("ANNEES CITEES dans la valeur (non retenues comme "
                        f"date) : {', '.join(str(a) for a in citees)}")
    else:
        lu.notes.append("aucune annee a quatre chiffres dans la valeur")
    return lu


def annees_de_description(texte):
    """-> liste triee de « YYYY » / « YYYY-MM » trouves dans une description.

    Un mois adjacent a une annee donne « YYYY-MM » ; une annee seule donne
    « YYYY ». Les deux formes coexistent quand la description porte les deux
    (« mars 2013 » et « 2013 » ailleurs) : le doublon est ecarte, la forme la
    plus precise gagne pour une annee donnee.
    """
    if not texte:
        return []
    aplati = plie(texte)
    mois_par_annee = collections.defaultdict(set)
    for m in RE_MOIS_ANNEE.finditer(aplati):
        mois_par_annee[int(m.group(2))].add(MOIS_TOUS[m.group(1)])
    trouvees = set()
    for annee in {int(a) for a in RE_ANNEE_LIBRE.findall(aplati)}:
        if not ANNEE_MIN <= annee <= ANNEE_MAX:
            continue
        mois = mois_par_annee.get(annee)
        if mois:
            for mo in mois:
                trouvees.add(f"{annee:04d}-{mo:02d}")
        else:
            trouvees.add(f"{annee:04d}")
    return sorted(trouvees)


def annee_de(jeton):
    """« 2018-12 » -> 2018 ; « 2018 » -> 2018 ; sinon None."""
    m = re.match(r'^(\d{4})', jeton or '')
    return int(m.group(1)) if m else None


# --------------------------------------------------------------------------
# inventaire
# --------------------------------------------------------------------------
def nettoie(texte):
    """Un champ CSV redige : ';' -> ',', espaces reduits, aucun saut de ligne."""
    return ' '.join(str(texte if texte is not None else '')
                    .replace(';', ',').split())


def nettoie_valeur(brute):
    """`raw_value` : la valeur TELLE QUELLE, seuls les blancs sont reduits.

    Contrairement a `nettoie`, le point-virgule est CONSERVE — 12 valeurs de
    `dateSource` en portent (« Sedgwick 2018b ; Sedgwick 2019g »), et le
    remplacer falsifierait la colonne qui doit precisement dire ce que le
    graphe contient. Le module csv se charge de guillemeter le champ ; le
    seul traitement applique est la reduction des blancs, pour qu'une ligne
    du CSV reste une ligne (aucune valeur du perimetre n'en contient, ce qui
    a ete verifie sur v111 — la reduction est une precaution, pas un
    correctif).
    """
    if brute is None:
        return ''
    return ' '.join(str(brute).split())


def noms_de_types(graphe):
    return {t['id']: (t.get('name') or t['id'])
            for t in (graphe.get('types') or []) if t.get('id')}


def inventaire(graphe, date_reference):
    """-> liste de dicts, une par (entite, cle datee). Triee, sans horodatage."""
    nom_type = noms_de_types(graphe)

    # --- type_key_mismatch : les types GRC-20 portes par chaque cle ---------
    types_par_cle = collections.defaultdict(collections.Counter)
    for entite in graphe.get('entities') or []:
        for cle, attribut in (entite.get('attributes') or {}).items():
            if cle in CLES_DATEES:
                types_par_cle[cle][type_grc20(attribut)] += 1

    lignes = []
    for entite in graphe.get('entities') or []:
        eid = entite.get('id')
        if not eid:
            continue
        attrs = entite.get('attributes')
        if not isinstance(attrs, dict):
            continue
        presentes = [c for c in CLES_DATEES if c in attrs]
        if not presentes:
            continue
        types = sorted(nom_type.get(t, t) for t in (entite.get('types') or []))
        indices = annees_de_description(
            valeur_brute(attrs.get('description')))
        annees_indice = {a for a in (annee_de(j) for j in indices)
                         if a is not None}

        lues = {}
        for cle in presentes:
            attribut = attrs[cle]
            lues[cle] = (attribut, analyse(cle, type_grc20(attribut),
                                           valeur_brute(attribut)))

        # --- conflits intra-entite, par ROLE (cf. docstring) ----------------
        annee_de_cle = {}
        for cle, (_a, lu) in lues.items():
            if lu.annees and lu.granularite != 'plage':
                annee_de_cle[cle] = lu.annees[0]
        conflits = {}          # cle -> texte de note
        for role in ROLES_COMPARABLES:
            membres = sorted(c for c in presentes
                             if ROLE_DE_CLE.get(c) == role
                             and c in annee_de_cle)
            annees = {annee_de_cle[c] for c in membres}
            if len(membres) > 1 and len(annees) > 1:
                detail = ', '.join(
                    f"{c}={lues[c][1].iso or annee_de_cle[c]}"
                    for c in membres)
                for c in membres:
                    conflits[c] = (
                        f"CONFLIT INTRA-ENTITE (role « {role} ») : les cles de "
                        f"meme role designent des annees differentes — "
                        f"{detail} ; signalement, aucune n'est declaree "
                        "fautive")

        # --- ecarts INTER-ROLE : reportes, jamais promus en conflit ---------
        # Chaque remarque n'est portee que par les DEUX lignes qu'elle
        # compare : la coller sur toutes les lignes de l'entite ferait dire
        # a `dateSource` quelque chose sur `dateEnd`, et un lecteur presse y
        # verrait un defaut de la ligne qu'il regarde.
        inter = collections.defaultdict(list)

        def note_inter(cle_a, cle_b, texte):
            inter[cle_a].append(texte)
            inter[cle_b].append(texte)

        debuts = {c: annee_de_cle[c] for c in presentes
                  if ROLE_DE_CLE.get(c) == 'debut' and c in annee_de_cle}
        fins = {c: annee_de_cle[c] for c in presentes
                if ROLE_DE_CLE.get(c) == 'fin' and c in annee_de_cle}
        for cd in sorted(debuts):
            for cf in sorted(fins):
                if debuts[cd] > fins[cf]:
                    note_inter(cd, cf,
                               f"ECART INTER-ROLE (non-verdict) : {cd}="
                               f"{lues[cd][1].iso} (role debut) est POSTERIEUR "
                               f"a {cf}={lues[cf][1].iso} (role fin)")
        points = {c: annee_de_cle[c] for c in presentes
                  if ROLE_DE_CLE.get(c) == 'point' and c in annee_de_cle}
        for cp in sorted(points):
            for autre in sorted(set(debuts) | set(fins)):
                annee_autre = debuts.get(autre, fins.get(autre))
                if annee_autre != points[cp]:
                    note_inter(cp, autre,
                               f"ECART INTER-ROLE (non-verdict) : {cp}="
                               f"{lues[cp][1].iso} (role point) et {autre}="
                               f"{lues[autre][1].iso} (role "
                               f"{ROLE_DE_CLE.get(autre)}) ne portent pas la "
                               "meme annee — roles differents, aucune "
                               "comparaison de verdict n'est faite")

        est_crypto = any(t in TYPES_CRYPTO for t in types)

        for cle in presentes:
            attribut, lu = lues[cle]
            notes = list(lu.notes)
            role = ROLE_DE_CLE.get(cle, 'point')
            if cle in CLES_NON_DATEES_DANS_LE_PERIMETRE:
                notes.insert(0, "cle du perimetre qui ne porte PAS une date : "
                             + CLES_NON_DATEES_DANS_LE_PERIMETRE[cle])
            if cle in conflits:
                notes.append(conflits[cle])
            elif role in ROLES_COMPARABLES and lu.annees:
                membres = [c for c in presentes
                           if ROLE_DE_CLE.get(c) == role and c != cle
                           and c in annee_de_cle]
                if membres:
                    notes.append(
                        f"role « {role} » : accord d'annee avec "
                        f"{', '.join(sorted(membres))}")
            notes.extend(inter.get(cle, []))

            # --- description ------------------------------------------------
            conflit_desc = ''
            if indices:
                annee_valeur = lu.annees[0] if lu.annees else None
                if annee_valeur is None:
                    notes.append(
                        "description datee mais aucune annee derivee de la "
                        "valeur : comparaison impossible, rien n'est conclu")
                else:
                    concernees = set(lu.annees)
                    if concernees & annees_indice:
                        conflit_desc = 'non'
                        notes.append(
                            f"description : accord d'annee "
                            f"({'|'.join(indices)} contre "
                            f"{lu.iso or ','.join(str(a) for a in lu.annees)})")
                    else:
                        conflit_desc = 'oui'
                        notes.append(
                            f"CONFLIT DESCRIPTION : la description ne cite que "
                            f"{'|'.join(indices)} la ou {cle} vaut "
                            f"{lu.iso or ','.join(str(a) for a in lu.annees)} "
                            "— une description cite volontiers des annees qui "
                            "ne sont pas la date de l'entite : signalement, "
                            "pas erreur etablie")

            # --- plausibilite ------------------------------------------------
            drapeau, autres = plausibilite(lu, est_crypto, types,
                                           date_reference)
            notes.extend(autres)

            lignes.append({
                'entity_id': eid,
                'entity_name': entite.get('name') or '',
                'entity_types': '|'.join(types),
                'attribute_key': cle,
                'grc20_value_type': type_grc20(attribut),
                'raw_value': valeur_brute(attribut),
                'normalized_iso': lu.iso,
                'granularity': lu.granularite,
                'format_family': lu.famille,
                'dmy_ambiguous': lu.dmy,
                'type_key_mismatch': 'oui' if len(types_par_cle[cle]) > 1
                                     else 'non',
                'intra_entity_conflict': 'oui' if cle in conflits else '',
                'description_date_hint': '|'.join(indices),
                'description_conflict': conflit_desc,
                'plausibility_flag': drapeau,
                'notes': ' | '.join(notes),
                '_role': role,
                '_types_cle': dict(types_par_cle[cle]),
            })

    lignes.sort(key=lambda x: (x['entity_id'], x['attribute_key']))
    return lignes


def plausibilite(lu, est_crypto, types, date_reference):
    """-> (drapeau, notes). Precedence STRICTE, cf. docstring."""
    notes = []
    if not lu.annees:
        return 'non_parsable', notes

    hors = [a for a in lu.annees if a < ANNEE_MIN or a > ANNEE_MAX]
    futur = False
    if lu.granularite == 'plage':
        futur = max(lu.annees) > date_reference.year
    elif lu.granularite == 'jour' and lu.iso and len(lu.iso) == 10:
        futur = datetime.date.fromisoformat(lu.iso) > date_reference
    elif lu.granularite == 'mois' and len(lu.iso) == 7:
        futur = lu.iso > date_reference.strftime('%Y-%m')
    else:
        futur = lu.annees[0] > date_reference.year

    ancien = False
    if est_crypto and lu.borne_min is not None:
        if lu.borne_min < SEUIL_CRYPTO:
            # une granularite trop grossiere ne prouve rien : l'annee 2008
            # seule peut tomber des deux cotes du 31/10/2008.
            if lu.granularite in ('annee', 'plage') and lu.annees[0] == 2008:
                notes.append(
                    "entite de type crypto datee de 2008 sans mois : le "
                    "31/10/2008 (livre blanc) tombe dans l'annee, la "
                    "granularite ne permet pas de trancher")
            elif lu.dmy == 'oui' and len(lu.lectures_possibles) == 2 \
                    and lu.lectures_possibles[1] >= SEUIL_CRYPTO:
                # Ordre jour/mois indecidable ET les deux lectures tombent de
                # part et d'autre du 31/10/2008 : drapeau non fonde. Trancher
                # reviendrait a appliquer une convention, ce que ce script
                # s'interdit partout ailleurs.
                notes.append(
                    "entite de type crypto dont l'ordre jour/mois est "
                    "indecidable : les deux lectures possibles "
                    f"({lu.lectures_possibles[0].isoformat()} ou "
                    f"{lu.lectures_possibles[1].isoformat()}) tombent de part "
                    "et d'autre du 31/10/2008 (livre blanc) — aucune des deux "
                    "n'etant etablie, l'anteriorite ne l'est pas non plus")
            elif lu.granularite == 'mois' and lu.iso == '2008-10':
                notes.append(
                    "entite de type crypto datee d'octobre 2008 : le "
                    "31/10/2008 tombe dans le mois, la granularite ne permet "
                    "pas de trancher")
            else:
                ancien = True

    if hors:
        if futur:
            notes.append("egalement posterieure a la date de reference "
                         f"{date_reference.isoformat()}")
        if ancien:
            notes.append("egalement anterieure au 31/10/2008 sur une entite "
                         f"crypto ({'|'.join(t for t in types if t in TYPES_CRYPTO)})")
        notes.append("annee(s) hors des bornes [1400, 2030] : "
                     + ', '.join(str(a) for a in hors))
        return 'annee_hors_plage', notes
    if futur:
        if ancien:
            notes.append("egalement anterieure au 31/10/2008 sur une entite "
                         "crypto")
        notes.append("posterieure a la date de reference gelee "
                     f"{date_reference.isoformat()}")
        return 'futur', notes
    if ancien:
        notes.append(
            f"date {lu.iso or lu.annees[0]} anterieure au 31/10/2008 (livre "
            "blanc Bitcoin) sur une entite de type "
            f"{'|'.join(t for t in types if t in TYPES_CRYPTO)}")
        return 'anterieure_a_2008_sur_entite_crypto', notes
    return 'ok', notes


# --------------------------------------------------------------------------
# CSV
# --------------------------------------------------------------------------
def en_lignes_csv(lignes):
    sorties = []
    for ligne in lignes:
        sortie = {c: nettoie(ligne[c]) for c in COLONNES}
        sortie['raw_value'] = nettoie_valeur(ligne['raw_value'])
        sorties.append(sortie)
    return sorties


def rend_csv(sorties):
    """-> le CSV en memoire, exactement tel qu'il serait ecrit sur disque."""
    tampon = io.StringIO(newline='')
    graveur = csv.DictWriter(tampon, fieldnames=list(COLONNES), delimiter=';',
                             lineterminator='\n')
    graveur.writeheader()
    graveur.writerows(sorties)
    return tampon.getvalue()


def ecrit_csv(chemin, contenu):
    dossier = os.path.dirname(os.path.abspath(chemin))
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    with open(chemin, 'w', encoding='utf-8', newline='') as f:
        f.write(contenu)


# --------------------------------------------------------------------------
# rapports
# --------------------------------------------------------------------------
def rapport(lignes, chemin_graphe, graphe, date_reference):
    entites = {x['entity_id'] for x in lignes}
    print(f"graphe  : {os.path.relpath(chemin_graphe, REPO)}")
    print(f"lignes  : {len(lignes)} couples (entite, cle datee)")
    print(f"entites : {len(entites)} distinctes en portent au moins un")
    print(f"cles    : {len(CLES_DATEES)} cles inventoriees ; exclue "
          f"explicitement : {', '.join(CLES_EXCLUES_NON_DATEES)} "
          "(page IMPRIMEE d'une section, pas une date)")
    print(f"reference de plausibilite : {date_reference.isoformat()} (GELEE)")

    par_cle = collections.Counter(x['attribute_key'] for x in lignes)
    print("\n=== PAR CLE ===")
    for cle in CLES_DATEES:
        types = collections.Counter(x['grc20_value_type'] for x in lignes
                                    if x['attribute_key'] == cle)
        detail = ', '.join(f"{t}:{n}" for t, n in sorted(types.items()))
        marque = '  [NE PORTE PAS UNE DATE]' \
            if cle in CLES_NON_DATEES_DANS_LE_PERIMETRE else ''
        print(f"  {cle:16s} {par_cle.get(cle, 0):4d}  {detail}{marque}")

    print("\n=== PAR format_family ===")
    familles = collections.Counter(x['format_family'] for x in lignes)
    for famille in FAMILLES:
        print(f"  {famille:26s} {familles.get(famille, 0):4d}")
    autres = sorted(set(familles) - set(FAMILLES))
    for famille in autres:
        print(f"  {famille:26s} {familles[famille]:4d}  (HORS NOMENCLATURE)")

    # `libre` est un fourre-tout par convention de colonne : le detailler
    # evite de faire passer une date en toutes lettres pour du texte opaque.
    libres = [x for x in lignes if x['format_family'] == 'libre']
    sous = collections.Counter()
    for x in libres:
        if x['granularity'] == 'jour':
            sous['date en toutes lettres (jour mois annee)'] += 1
        elif x['granularity'] == 'mois':
            sous['mois en toutes lettres + annee'] += 1
        elif x['granularity'] == 'plage':
            sous['plage a deux bornes datees'] += 1
        else:
            sous['texte non normalisable'] += 1
    print("  --- detail de `libre`")
    for nom, n in sorted(sous.items()):
        print(f"      {n:4d}  {nom}")

    print("\n=== PAR granularity ===")
    granularites = collections.Counter(x['granularity'] for x in lignes)
    for g in GRANULARITES:
        print(f"  {g:16s} {granularites.get(g, 0):4d}")

    print("\n=== PAR plausibility_flag ===")
    drapeaux = collections.Counter(x['plausibility_flag'] for x in lignes)
    for d in PLAUSIBILITES:
        print(f"  {d:38s} {drapeaux.get(d, 0):4d}")

    print("\n=== SIGNALEMENTS ===")
    print(f"  dmy_ambiguous=oui        "
          f"{sum(1 for x in lignes if x['dmy_ambiguous'] == 'oui'):4d}")
    print(f"  type_key_mismatch=oui    "
          f"{sum(1 for x in lignes if x['type_key_mismatch'] == 'oui'):4d}")
    print(f"  intra_entity_conflict    "
          f"{sum(1 for x in lignes if x['intra_entity_conflict'] == 'oui'):4d}")
    print(f"  description_conflict=oui "
          f"{sum(1 for x in lignes if x['description_conflict'] == 'oui'):4d}")
    print(f"  description_conflict=non "
          f"{sum(1 for x in lignes if x['description_conflict'] == 'non'):4d}")
    print(f"  avec description_date_hint "
          f"{sum(1 for x in lignes if x['description_date_hint']):4d}")

    mismatch = sorted({(x['attribute_key'],
                        tuple(sorted(x['_types_cle'].items())))
                       for x in lignes if x['type_key_mismatch'] == 'oui'})
    if mismatch:
        print("  --- cles a types GRC-20 melanges")
        for cle, types in mismatch:
            print(f"      {cle:16s} "
                  + ', '.join(f"{t}:{n}" for t, n in types))

    for drapeau in ('futur', 'anterieure_a_2008_sur_entite_crypto',
                    'annee_hors_plage'):
        cas = [x for x in lignes if x['plausibility_flag'] == drapeau]
        print(f"\n=== {drapeau.upper()} ({len(cas)}) ===")
        if not cas:
            print("  (aucun)")
        for x in cas:
            print(f"  {x['entity_id']} {x['attribute_key']:16s} "
                  f"{x['raw_value']!r}  [{x['entity_types']}] "
                  f"{nettoie(x['entity_name'])[:60]}")

    conflits = [x for x in lignes if x['intra_entity_conflict'] == 'oui']
    print(f"\n=== intra_entity_conflict ({len(conflits)}) ===")
    if not conflits:
        print("  (aucun)")
    for x in conflits:
        print(f"  {x['entity_id']} {x['attribute_key']:16s} "
              f"{x['raw_value']!r} — {nettoie(x['entity_name'])[:50]}")

    desc = [x for x in lignes if x['description_conflict'] == 'oui']
    print(f"\n=== description_conflict ({len(desc)}) ===")
    if not desc:
        print("  (aucun)")
    for x in desc:
        print(f"  {x['entity_id']} {x['attribute_key']:16s} "
              f"{x['raw_value']!r} contre description "
              f"{x['description_date_hint']} — "
              f"{nettoie(x['entity_name'])[:45]}")

    print("\n=== ENTITES PORTANT LE PLUS DE CLES DATEES ===")
    par_entite = collections.Counter(x['entity_id'] for x in lignes)
    noms = {x['entity_id']: (nettoie(x['entity_name']),
                             x['entity_types']) for x in lignes}
    cles_par_entite = collections.defaultdict(list)
    for x in lignes:
        cles_par_entite[x['entity_id']].append(x['attribute_key'])
    combien = collections.Counter(par_entite.values())
    print("  distribution : "
          + ', '.join(f"{n} cle(s) -> {combien[n]} entites"
                      for n in sorted(combien, reverse=True)))
    maximum = max(par_entite.values()) if par_entite else 0
    exaequo = combien.get(maximum, 0)
    # Un « top 10 » sur un maximum atteint par des dizaines d'entites est un
    # artefact du tri, pas un resultat : le dire evite de faire croire que
    # les dix nommees se distinguent.
    print(f"  maximum : {maximum} cles datees, atteint par {exaequo} entites "
          "EX AEQUO — les dix ci-dessous sont les premieres par id, elles ne "
          "se distinguent pas des autres ex aequo")
    for eid, n in sorted(par_entite.items(),
                         key=lambda kv: (-kv[1], kv[0]))[:10]:
        nom, types = noms[eid]
        print(f"  {n:2d}  {eid} [{types}] {nom[:44]}")
        print(f"      {', '.join(sorted(cles_par_entite[eid]))}")
    # Les combinaisons de cles, elles, sont un resultat : elles disent quels
    # profils temporels le graphe pratique reellement.
    profils = collections.Counter(
        tuple(sorted(cles)) for cles in cles_par_entite.values())
    print("  --- combinaisons de cles datees observees")
    for profil, n in sorted(profils.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"      {n:4d}  {'|'.join(profil)}")

    veille(graphe)


def veille(graphe):
    """Les cles HORS perimetre dont la valeur ressemble a une date.

    Heuristique DECLAREE (cf. docstring) : valeur courte contenant une annee
    de 1500 a 2049. Elle n'alimente que ce bloc, jamais le CSV — le perimetre
    d'un inventaire ne doit pas bouger tout seul.
    """
    trouvees = collections.defaultdict(list)
    totaux = collections.Counter()
    for entite in graphe.get('entities') or []:
        for cle, attribut in (entite.get('attributes') or {}).items():
            if cle in CLES_DATEES or cle in CLES_EXCLUES_NON_DATEES:
                continue
            totaux[cle] += 1
            brute = valeur_brute(attribut)
            if isinstance(brute, bool) or brute is None:
                continue
            texte = ' '.join(str(brute).split())
            if len(texte) > VEILLE_LONGUEUR_MAX:
                continue
            if RE_VEILLE.search(texte):
                trouvees[cle].append((texte, analyse(cle, type_grc20(attribut),
                                                     brute)))
    # Deux paliers, parce que « contenir une annee » et « etre une date » ne
    # sont pas la meme chose : `cveId` (« CVE-2010-5137 ») et `rauchs2016Ref`
    # portent une annee sans etre des dates, `founded` (« 1992 ») et
    # `publicDisclosure` (« 01/03/2013 ») en sont. Le palier est celui du
    # niveau 1 de normalisation, deja defini pour le perimetre — pas un
    # nouveau jugement.
    etablies, citations = [], []
    for cle, valeurs in trouvees.items():
        total = totaux[cle]
        if not total or len(valeurs) / total < 0.75:
            continue
        datees = [t for t, lu in valeurs if lu.iso or lu.granularite == 'plage']
        apercu = sorted({t for t, _ in valeurs})
        entree = (len(valeurs), total, len(datees), cle, apercu)
        if datees and len(datees) / len(valeurs) >= 0.5:
            etablies.append(entree)
        else:
            citations.append(entree)
    etablies.sort(key=lambda x: (-x[0], x[3]))
    citations.sort(key=lambda x: (-x[0], x[3]))
    print("\n=== VEILLE : cles DATEES HORS PERIMETRE (jamais dans le CSV) ===")
    print("  heuristique declaree : valeur de moins de "
          f"{VEILLE_LONGUEUR_MAX} caracteres contenant une annee 1500-2049, "
          "sur >= 75 %")
    print("  des valeurs de la cle. Palier 1 : la moitie au moins de ces "
          "valeurs est normalisable")
    print("  au niveau 1 (donc: des dates). Arbitrage auteur : faut-il "
          "elargir le perimetre ?")
    print(f"  --- PALIER 1, formes datees etablies ({len(etablies)} cles)")
    if not etablies:
        print("      (aucune)")
    for n, total, datees, cle, apercu in etablies:
        print(f"      {n:3d}/{total:<3d} ({datees} normalisables) {cle:20s} "
              + ' | '.join(apercu[:4])[:80])
    print(f"  --- PALIER 2, annee CITEE sans forme de date ({len(citations)} "
          "cles) : probablement hors sujet")
    if not citations:
        print("      (aucune)")
    for n, total, _d, cle, apercu in citations:
        print(f"      {n:3d}/{total:<3d} {cle:20s} "
              + ' | '.join(apercu[:3])[:80])


def controle(lignes, chemin_csv, contenu):
    """`--check` : 1 des que le CSV verse differe du CSV regenere."""
    if not os.path.exists(chemin_csv):
        print(f"ECHEC (donnees) : CSV d'inventaire absent : "
              f"{os.path.relpath(chemin_csv, REPO)} — le regenerer avec "
              "`--csv`", file=sys.stderr)
        return CODE_DIVERGENCE
    try:
        with open(chemin_csv, encoding='utf-8', newline='') as f:
            verse = f.read()
    except (OSError, UnicodeDecodeError) as err:
        echec_invocation(f"CSV d'inventaire illisible : {err}")
    if verse == contenu:
        print(f"OK : {os.path.relpath(chemin_csv, REPO)} est identique au CSV "
              f"regenere depuis le graphe ({len(lignes)} lignes).")
        return 0
    verses = verse.splitlines()
    regeneres = contenu.splitlines()
    print(f"ECHEC (donnees) : {os.path.relpath(chemin_csv, REPO)} diverge du "
          f"CSV regenere ({len(verses)} lignes versees, {len(regeneres)} "
          "regenerees).", file=sys.stderr)
    montrees = 0
    for numero, (a, b) in enumerate(zip(verses, regeneres), start=1):
        if a != b and montrees < 10:
            montrees += 1
            print(f"  ligne {numero} verse    : {a[:200]}", file=sys.stderr)
            print(f"  ligne {numero} regenere : {b[:200]}", file=sys.stderr)
    if len(verses) != len(regeneres):
        surplus = verses[len(regeneres):] or regeneres[len(verses):]
        cote = 'verse' if len(verses) > len(regeneres) else 'regenere'
        for ligne in surplus[:10]:
            print(f"  seulement dans le {cote} : {ligne[:200]}",
                  file=sys.stderr)
    return CODE_DIVERGENCE


# --------------------------------------------------------------------------
def main(argv=None):
    p = argparse.ArgumentParser(
        description="Inventorie les 24 cles d'attribut DATEES du graphe "
                    "GRC-20 : une ligne par (entite, cle), avec sa forme, sa "
                    "granularite, son ambiguite jour/mois et ses conflits. "
                    "Lecture seule du graphe : ce script n'ecrit jamais un "
                    "graphe, une carte ou un patch. Sans --csv, il n'ecrit "
                    "rien du tout.",
        epilog="Codes de sortie : 0 = l'inventaire a tourne (des valeurs non "
               "parsables et des conflits sont un RESULTAT) ; 1 = --check a "
               "trouve une divergence ; 2 = erreur d'invocation. `page_start` "
               "est exclue explicitement : elle porte une page IMPRIMEE, pas "
               "une date. Aucun jour n'est devine sur une valeur NN/NN/AAAA "
               "ambigue : normalized_iso s'arrete a l'annee. Les conflits "
               "sont des SIGNALEMENTS, jamais des verdicts.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--graph', default=None, metavar='FICHIER',
                   help="graphe inventorie (defaut : le plus recent du depot)")
    p.add_argument('--csv', nargs='?', const=CSV_AUTO, default=None,
                   metavar='CHEMIN',
                   help="ECRIT le CSV d'inventaire (';'-separe). Sans valeur, "
                        "le nom est DERIVE de la version du graphe "
                        "(docs/audits/data/chronology-date-inventory-vNNN.csv)"
                        ", pour qu'un inventaire de v112 n'ecrase pas la "
                        "preuve v111. Omettre l'option = aucune ecriture. "
                        "INCOMPATIBLE avec --check : --csv PRODUIT la preuve, "
                        "--check la LIT")
    p.add_argument('--check', action='store_true',
                   help="compare le CSV verse au CSV regenere depuis le "
                        "graphe et sort en code 1 s'ils different (controle "
                        "de CI). N'ecrit rien. INCOMPATIBLE avec --csv")
    p.add_argument('--aujourdhui', default=None, metavar='AAAA-MM-JJ',
                   help="date de reference du drapeau `futur` (defaut : "
                        f"{DATE_REFERENCE.isoformat()}, GELEE pour que deux "
                        "executions rendent le meme CSV — ne la changer que "
                        "sciemment, elle modifie la sortie)")
    args = p.parse_args(argv)

    if args.check and args.csv is not None:
        # Meme arbitrage que dans audit_section_page_start.py : --check
        # COMPARE le graphe a la preuve deja enregistree et n'ecrit rien ;
        # --csv PRODUIT cette preuve. Les combiner rendrait le controle
        # tautologique (on comparerait le CSV a lui-meme, tout juste ecrit).
        echec_invocation(
            "--check et --csv ne se combinent pas : --check compare le CSV "
            "verse au CSV regenere (aucune ecriture), --csv produit ce CSV. "
            "Lancer les deux separement : d'abord `--csv`, puis `--check`")

    date_reference = DATE_REFERENCE
    if args.aujourdhui:
        try:
            date_reference = datetime.date.fromisoformat(args.aujourdhui)
        except ValueError:
            echec_invocation("--aujourdhui attend une date AAAA-MM-JJ : "
                             f"{args.aujourdhui!r}")

    chemin_graphe = args.graph or graphe_le_plus_recent()
    if not chemin_graphe:
        echec_invocation("aucun graphe grc20-these-mael-rolland-v*.json dans "
                         "le depot (et aucun --graph fourni)")
    graphe = lire_json(chemin_graphe, 'graphe inventorie')
    if not isinstance(graphe, dict) or not isinstance(
            graphe.get('entities'), list):
        echec_invocation(f"graphe sans liste d'entites : {chemin_graphe}")

    chemin_csv_defaut = csv_defaut(chemin_graphe)
    if args.csv == CSV_AUTO:
        args.csv = chemin_csv_defaut

    lignes = inventaire(graphe, date_reference)
    contenu = rend_csv(en_lignes_csv(lignes))

    if args.check:
        return controle(lignes, chemin_csv_defaut, contenu)

    rapport(lignes, chemin_graphe, graphe, date_reference)

    if args.csv:
        ecrit_csv(args.csv, contenu)
        print(f"\nCSV d'inventaire ecrit : {os.path.relpath(args.csv, REPO)} "
              f"({len(lignes)} lignes)")
    else:
        print("\n(aucune ecriture — passer --csv pour produire le CSV "
              "d'inventaire)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
