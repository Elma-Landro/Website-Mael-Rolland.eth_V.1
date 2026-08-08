#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit des `page_start` des noeuds de section, contre les PDF imprimes — LECTURE SEULE DU GRAPHE.

POURQUOI CE SCRIPT EXISTE. La migration SourceQuote est gelee parce que les
`page_start` portes par le graphe contredisent le texte imprime : la PR #115
a etabli que `II.3.2` declare p. 202 alors que son titre est imprime p. 190,
et que `III.1.2.b` declare p. 265 pour un titre imprime p. 243. Tant que
l'ampleur exacte de cet ecart n'est pas mesuree, aucune citation ne peut etre
gravee avec une pagination. Ce script mesure — il ne repare pas.

CE QU'IL N'ECRIT JAMAIS : le graphe, aucune carte d'ancrage, aucun patch.
Sa seule ecriture possible est le CSV de diagnostic, et seulement quand
`--csv` est passe. Sans `--csv`, il est integralement en lecture seule.

=====================================================================
LES TROIS PIEGES METHODOLOGIQUES, ET CE QUI LES CONTIENT ICI
=====================================================================

PIEGE 1 — PAGE IMPRIMEE != OFFSET DE FICHIER PDF. Les PDF du depot sont
decoupes par bloc (`4_Introduction_generale.pdf`, `5_Chapitre_1.pdf`, …) :
l'offset d'une page dans son fichier n'a aucun rapport avec sa pagination
dans la these. Ce script ne deduit JAMAIS une page d'un offset. Il CALIBRE :
chaque page du corps porte son numero imprime dans un pied de page de la
forme « — NN — », que pypdf extrait ; le script lit ce numero page par page
et ne travaille qu'en pages IMPRIMEES.

  Calibration constatee sur les PDF du depot (et re-verifiee a chaque
  execution, cf. `--check` et le bloc CALIBRATION du rapport) :
    1_Premières_pages.pdf        pages imprimees 1-5 (+ 1 couverture
                                 SANS numero imprime — signalee, jamais
                                 devinee)
    2_Tables_des_matieres.pdf    6-12      (EXCLU de la recherche de titres,
                                            cf. plus bas)
    3_Precautions_ecriture.pdf   13-14
    4_Introduction_generale.pdf  15-51
    5_Chapitre_1.pdf             52-141
    6_Chapitre_2.pdf             142-219
    7_Chapitre_3.pdf             220-331
    8_Conclusion_Generale.pdf    332-340
  La suite 1..340 est continue et sans trou. Toute page portant zero ou
  plusieurs marques « — NN — » est signalee dans le rapport et ecartee de
  l'index : une page dont le numero est illisible ne prouve rien.

PIEGE 2 — UNE SECTION PARENTE COMMENCE LEGITIMEMENT AVANT SES ENFANTS.
`II.3` p. 185 et `II.3.1` p. 186 n'est pas une incoherence. Ce script ne
compare donc JAMAIS un `page_start` a celui d'une autre section : il le
compare a la page ou le titre de CETTE section est imprime, et rien d'autre.
Les colonnes `parent` / `page_start_parent` sont fournies pour la lecture
humaine, pas pour le verdict. Le seul cas ou la relation parent/enfant
produit une remarque est l'inverse — une parente dont le `page_start` est
POSTERIEUR a celui de son premier enfant — et cette remarque va dans `note`,
jamais dans `statut`.

PIEGE 3 — LA PAGINATION N'EST JAMAIS DICTEE PAR CE QUI ARRANGERAIT LES
SOURCEQUOTE. Le dossier `docs/audits/data/sourcequote-migration-verification-v1.csv`
n'est lu que pour remplir la colonne `concernee_sourcequote` (oui/non). Il
n'intervient dans AUCUNE decision de page, ne pondere aucun candidat, et
n'est meme pas charge quand `--check` tourne. Si le resultat contrarie les
41 ops, c'est le texte imprime qui a raison.

=====================================================================
LA REGLE DE PREUVE — ce qui remplit `page_imprimee_verifiee`
=====================================================================
UNE SEULE SOURCE remplit cette colonne : un TITRE IMPRIME dans le CORPS de
la these. Concretement, le script indexe toutes les fenetres de 1 a 4 lignes
consecutives de chaque page du corps, et cherche une EGALITE EXACTE entre la
forme reduite d'une fenetre et la forme reduite d'une denomination du noeud.

  Forme reduite (`reduit`) : accents deplies, minuscules, puis TOUT ce qui
  n'est pas [a-z0-9] supprime — espaces compris. C'est ce qui absorbe les
  artefacts d'extraction PDF (« d e l'enregistrement », « premier s
  contacts »), les petites capitales (« I N T R O D U C T I O N ») et les
  variantes typographiques d'apostrophe ou de tiret. C'est une egalite, pas
  une approximation.

  Denominations essayees (toutes reduites, doublons ecartes) : `name`,
  `labelFr`, `title`, chacune AUSSI privee de son prefixe de numerotation
  (`I.1.1.a`, `A.1.`, `1)`, `a)`) et, quand le nom commence par une glose
  courte suivie d'un tiret cadratin, la partie qui suit ce tiret
  (« Conclusion — Resume de la these » -> « Resume de la these »). Le
  prefixe est retire des DEUX cotes : les titres de troisieme niveau sont
  imprimes sans numerotation dans la these, et l'introduction numerote
  « 1) », « 2) » la ou le graphe ecrit « A.1. », « A.2. ».

  `2_Tables_des_matieres.pdf` est EXCLU de cet index. La table des matieres
  contient tous les titres : l'y chercher rendrait un resultat pour chaque
  section et ne prouverait rien sur l'endroit ou la section commence.

  Une egalite sur PLUSIEURS pages distinctes ne tranche pas : le statut
  devient `ambigu` et la colonne reste vide. Aucune heuristique ne choisit.

CE QUI NE REMPLIT PAS LA COLONNE, ET POURQUOI. Trois sources sont lues,
rapportees dans `note` sous le marqueur explicite « PISTE », et n'entrent
dans aucun verdict :

  - LA TABLE DES MATIERES IMPRIMEE (pages 6-12). Elle declare une page pour
    chaque titre, et sert de CORROBORATION independante : le rapport compte
    les accords et nomme les desaccords. Elle ne remplit pas la colonne
    parce qu'elle porte ses propres erreurs — la these y numerote deux fois
    « I.2.1 » (p. 89 et p. 100) et ecrit « II.2.3 » pour III.2.3 (p. 277).
    Une source qui se trompe sur la numerotation ne peut pas etre l'arbitre
    d'une numerotation.
  - LE QUASI-TITRE (difflib >= --piste-seuil sur une fenetre de titre). Le
    titre du graphe est parfois une reformulation du titre imprime
    (« A. La gouvernance des cryptomonnaies … » face a « A. LA GOUVERNANCE
    DES CM … », « Les CM : boucs emissaires … » face a « LES CM : BOUCS
    EMISSAIRES COMMODES … »). Une reformulation plausible n'est pas une
    preuve : c'est la lecon « Florence Dufy » du depot. Elle est donnee a
    l'auteur comme piste, jamais promue en verdict.
  - LE PREFIXE COMMUN (>= --piste-prefixe caracteres reduits, second filet
    quand difflib ne rend rien). Le graphe RACCOURCIT parfois un titre
    long : « « Creuser au fond du terrier » : les recherches
    documentaires » contre un titre imprime qui continue par « …, une
    source essentielle de connaissance de ce champ ». difflib note cela
    trop bas ; le prefixe commun le retrouve. Meme regime : piste, pas
    preuve.

=====================================================================
LES STATUTS — precedence STRICTE, dans cet ordre
=====================================================================
  1. `hors-perimetre` — noeud de type `Chapter`. La pagination d'un chapitre
     repond a une autre logique que celle d'une section : le titre de
     chapitre est imprime sur une page de garde qui n'est pas la premiere
     page de son contenu, et aucun de ces 5 noeuds ne porte de `page_start`.
     Le titre est quand meme cherche et la page trouvee reportee, pour
     information ; `--check` ne les regarde jamais.
  2. `absent` — le noeud ne porte pas de `page_start`. C'est une donnee, pas
     un vide : ces lignes disent quelles sections POURRAIENT en recevoir un,
     et leur `page_imprimee_verifiee` est remplie quand le titre est trouve.
  3. `ambigu` — le noeud porte un `page_start` mais la page imprimee n'est
     pas etablie : titre introuvable, ou plusieurs pages en egalite exacte.
     Rien n'est compare, rien n'est tranche.
  4. `incoherent` / `correct` — `page_start` present ET page imprimee
     etablie : ils different, ou ils coincident.

`ecart` = `page_start_actuel` - `page_imprimee_verifiee`, signe, et rempli
seulement quand les deux sont connus (donc jamais sur `absent` ni `ambigu`).

=====================================================================
LES CAUSES portees par `note` — constatees, jamais supposees
=====================================================================
  « sequelle de renumerotation v100-v106 (la cle a change de sens) —
      PROUVE » : le noeud portait une AUTRE `section_key` dans le graphe de
      reference historique (le plus ancien du depot, anterieur aux deux
      migrations), et son `page_start` est EXACTEMENT la page imprimee de
      cette ancienne cle. Autrement dit : la valeur a suivi le NOEUD, la
      renumerotation a change la SECTION que le noeud designe, et personne
      n'a deplace la page. La note nomme l'ancienne cle, le fichier de
      reference et la bonne page. C'est une egalite verifiable, pas une
      inference — sans elle, aucune note n'est posee.
  « erreur mecanique de pagination » : residu. La valeur declaree est la
      page imprimee d'une AUTRE section, nommee dans la note, sans que
      l'histoire des cles l'explique. Bucket volontairement distinct du
      precedent : confondre les deux ferait passer une coincidence pour une
      preuve.
  « numerotation IMPRIMEE differente de section_key » : la these imprime en
      tete du titre trouve un numero autre que `section_key` (elle numerote
      par exemple deux sections « I.2.1 »). Le script rapporte les deux et
      ne tranche pas laquelle a raison — sur quatre cas verifies en PR #115,
      c'est la cle brute qui avait raison contre la carte de renumerotation.
  « titre partage avec un autre noeud » : deux noeuds du graphe portent le
      meme titre reduit. Une reparation mecanique leur donnerait la meme
      page sans que personne ne le voie.
  « parente legitimement anterieure » : pose sur une parente correcte dont
      la page precede celle de son premier enfant — pour dire explicitement
      que ce n'est PAS une anomalie. La remarque inverse (« parente
      POSTERIEURE a son premier enfant — suspect ») est posee quand elle
      s'observe.
  « reellement ambigu » : accompagne tout statut `ambigu`, avec ce qui le
      rend ambigu.
  Aucune note n'attribue un ecart a v108-v109, et c'est un CONSTAT, pas une
  prudence : la comparaison des snapshots v96 a v110 montre que l'attribut
  `page_start` n'a change dans AUCUN des deux (0 valeur modifiee en v108, 0
  en v109 ; v110 n'a fait que retyper « 58 » en 58). v108 et v109 ont
  realigne des `section_key` PORTES PAR DES RELATIONS `appears in section`
  et le cablage des charges d'ancrage, pas l'attribut `page_start` des
  noeuds.

=====================================================================
`--check` — le mode qui servira APRES une eventuelle reparation
=====================================================================
Il ne produit ni CSV ni rapport long : il compare, pour chaque noeud portant
un `page_start` ET une page imprimee etablie, l'un a l'autre, et sort en
code 1 des la premiere divergence. C'est le controle qui devra rester vert
une fois la reparation appliquee — il existe des maintenant pour que la
reparation soit prouvable, et pas seulement annoncee.

REPLI SI pypdf EST ABSENT. pypdf est deja une dependance de fait du depot
(`docs/audits/` en vit). S'il manque, aucune page imprimee ne peut etre
etablie : la generation du CSV echoue alors en code 2, avec le message
d'installation. `--check` seul se replie sur le CSV de diagnostic deja
produit et versionne, dont il relit la colonne `page_imprimee_verifiee` :
le controle reste possible sur machine nue, en disant explicitement qu'il
s'appuie sur une preuve enregistree et non re-mesuree.

CODES DE SORTIE : 0 = l'audit a tourne (des `incoherent` restent un
resultat, pas une panne) ; 1 = `--check` a trouve au moins une divergence ;
2 = erreur d'invocation (graphe/PDF/CSV illisible, pypdf absent la ou il est
indispensable).

Usage:
    python3 scripts/audit_section_page_start.py
    python3 scripts/audit_section_page_start.py --csv
    python3 scripts/audit_section_page_start.py --csv /tmp/diag.csv
    python3 scripts/audit_section_page_start.py --check
"""
import argparse
import collections
import csv
import difflib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import (REPO, graphe_le_plus_recent, graphes_tries,  # noqa: E402
                          numero_de_version, sans_accents, TYPES_SECTION)

CODE_DIVERGENCE = 1
CODE_INVOCATION = 2

TYPE_CHAPITRE = 'Chapter'
TYPES_AUDITES = TYPES_SECTION + (TYPE_CHAPITRE,)

DOSSIER_PDF = os.path.join(REPO, 'assets', 'pdf')
CSV_AUTO = '<auto>'   # sentinelle : nom derive de la version du graphe


def csv_defaut(chemin_graphe):
    """Nom du CSV derive de la VERSION du graphe audite.

    Fige sur v110, le chemin par defaut aurait reecrit la preuve v110 avec
    des donnees v111 des qu'un graphe plus recent existe — et le repli sans
    pypdf aurait compare v111 a une preuve etablie pour v110."""
    version = numero_de_version(chemin_graphe or '')
    suffixe = f"v{version}" if version is not None else 'vX'
    return os.path.join(REPO, 'docs', 'audits', 'data',
                        f'section-page-start-diagnostic-{suffixe}.csv')
SOURCEQUOTE_DEFAUT = os.path.join(
    REPO, 'docs', 'audits', 'data',
    'sourcequote-migration-verification-v1.csv')

# Le corps de la these : les fichiers ou un titre de section peut etre
# IMPRIME a l'endroit ou la section commence. La table des matieres en est
# volontairement absente (cf. docstring).
PDF_CORPS = (
    '1_Premières_pages.pdf',
    '3_Precautions_ecriture.pdf',
    '4_Introduction_generale.pdf',
    '5_Chapitre_1.pdf',
    '6_Chapitre_2.pdf',
    '7_Chapitre_3.pdf',
    '8_Conclusion_Generale.pdf',
)
PDF_TDM = '2_Tables_des_matieres.pdf'

# Le pied de page qui porte la pagination imprimee de la these.
MARQUE_PAGE = re.compile(r'—\s*(\d+)\s*—')

# Prefixe de numerotation en tete de titre, retire des DEUX cotes :
#   « I.1.1.a », « III.2 », « A.1. », « B.1.a. », « 1) », « a) », « 2. »
PREFIXE_NUM = re.compile(
    r'^\s*(?:[IVX]+|[A-Z]|\d{1,2}|[a-z])'
    r'(?:\s*[.‑-]\s*(?:\d{1,2}|[a-z]))*'
    r'\s*[.)]?\s+')
# La numerotation reellement IMPRIMEE en tete d'un titre trouve (pour la
# comparer a `section_key`). Volontairement plus etroite : on ne veut pas
# prendre « Nous » pour une numerotation.
NUM_IMPRIMEE = re.compile(r'^\s*((?:[IVX]+|[A-E])(?:\.[0-9a-z]+)*)\s*[.)]?\s+')
# Glose editoriale suivie d'un tiret cadratin : « Conclusion — Resume … ».
GLOSE_TIRET = re.compile(r'^\s*\S{1,20}\s*[–—]\s+')

FENETRE_MAX = 4          # lignes consecutives agregees pour former un titre
PISTE_SEUIL_DEFAUT = 0.82
PISTE_MAX_DEFAUT = 3
PISTE_PREFIXE_DEFAUT = 16
# Une fenetre trop courte ou trop longue par rapport au titre cherche ne
# peut pas etre ce titre : filtre de longueur avant tout calcul difflib.
PISTE_LONGUEUR_MIN = 0.55
PISTE_LONGUEUR_MAX = 1.80

COLONNES = ('section_key', 'entity_id', 'nom_actuel', 'type',
            'page_start_actuel', 'page_imprimee_verifiee', 'ecart', 'statut',
            'source_preuve', 'parent', 'page_start_parent',
            'concernee_sourcequote', 'note')

STATUTS = ('correct', 'incoherent', 'absent', 'ambigu', 'hors-perimetre')

TITRE_INTROUVABLE = 'titre introuvable'


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


def importe_pypdf():
    """-> module pypdf, ou None. Le repli est decide par l'appelant."""
    try:
        import pypdf
        return pypdf
    except ImportError:
        return None


# --------------------------------------------------------------------------
# normalisation
# --------------------------------------------------------------------------
def reduit(s):
    """« II.3.2 Quand les CM réactivent… » -> « ii32quandlescmreactivent… ».

    Accents deplies, minuscules, puis suppression de tout ce qui n'est pas
    [a-z0-9] — espaces compris. Cf. docstring : c'est ce qui absorbe les
    artefacts d'extraction PDF et les petites capitales espacees.
    """
    return re.sub(r'[^a-z0-9]', '', sans_accents(s or '').lower())


def valeur_texte(attribut):
    """La valeur d'un attribut GRC-20, qu'il soit {type, value} ou brut."""
    if isinstance(attribut, dict):
        return attribut.get('value')
    return attribut


def entier_ou_none(valeur):
    """-> int, ou None si la valeur n'est pas un entier exploitable."""
    if valeur is None:
        return None
    if isinstance(valeur, bool):
        return None
    if isinstance(valeur, int):
        return valeur
    texte = str(valeur).strip()
    return int(texte) if re.fullmatch(r'-?\d+', texte) else None


def denominations(entite):
    """Les formes reduites sous lesquelles le titre du noeud peut etre imprime.

    -> liste triee de chaines reduites, sans doublon (tri = determinisme).
    """
    attrs = entite.get('attributes')
    if not isinstance(attrs, dict):
        attrs = {}
    brutes = [entite.get('name')]
    for cle in ('labelFr', 'title'):
        brutes.append(valeur_texte(attrs.get(cle)))
    formes = set()
    for brute in brutes:
        if not brute or not str(brute).strip():
            continue
        texte = str(brute)
        variantes = [texte, PREFIXE_NUM.sub('', texte)]
        sans_glose = GLOSE_TIRET.sub('', texte)
        if sans_glose != texte:
            variantes.append(sans_glose)
            variantes.append(PREFIXE_NUM.sub('', sans_glose))
        for variante in variantes:
            forme = reduit(variante)
            if len(forme) >= 8:      # sous 8 caracteres, tout collisionne
                formes.add(forme)
    return sorted(formes)


# --------------------------------------------------------------------------
# calibration des PDF (PIEGE 1)
# --------------------------------------------------------------------------
class Corpus:
    """Les pages du corps, indexees par leur numero IMPRIME."""

    def __init__(self):
        self.pages = []          # [(fichier, page_imprimee, [lignes])]
        self.anomalies = []      # pages sans numero imprime, ou avec plusieurs
        self.etendues = {}       # fichier -> (premiere, derniere)
        self.tdm = []            # [(page_imprimee, texte)] de la table

    def charge(self, pypdf, dossier):
        for fichier in PDF_CORPS + (PDF_TDM,):
            chemin = os.path.join(dossier, fichier)
            if not os.path.exists(chemin):
                echec_invocation(f"PDF canonique introuvable : {chemin}")
            try:
                lecteur = pypdf.PdfReader(chemin)
            except Exception as err:                  # noqa: BLE001
                echec_invocation(f"PDF illisible ({fichier}) : {err}")
            numeros = []
            for offset, page in enumerate(lecteur.pages):
                try:
                    texte = page.extract_text() or ''
                except Exception as err:              # noqa: BLE001
                    echec_invocation(
                        f"extraction impossible ({fichier}, offset {offset}) :"
                        f" {err}")
                marques = MARQUE_PAGE.findall(texte)
                if len(marques) != 1:
                    self.anomalies.append(
                        (fichier, offset, len(marques),
                         'aucune marque « — NN — »' if not marques
                         else f"{len(marques)} marques « — NN — »"))
                    continue
                imprimee = int(marques[0])
                numeros.append(imprimee)
                lignes = [' '.join(ligne.split())
                          for ligne in texte.split('\n')]
                lignes = [ligne for ligne in lignes if ligne]
                if fichier == PDF_TDM:
                    self.tdm.append((imprimee, lignes))
                else:
                    self.pages.append((fichier, imprimee, lignes))
            if numeros:
                self.etendues[fichier] = (min(numeros), max(numeros))
        self.pages.sort(key=lambda x: (x[1], x[0]))
        self.tdm.sort()

    def trous(self):
        """Les numeros imprimes manquants dans la suite couverte. Deterministe."""
        vus = sorted({p for _, p, _ in self.pages} | {p for p, _ in self.tdm})
        if not vus:
            return []
        return [n for n in range(vus[0], vus[-1] + 1) if n not in set(vus)]


def index_titres(corpus):
    """-> {forme_reduite: {(fichier, page_imprimee)}} sur les fenetres de titre.

    Une fenetre = 1 a FENETRE_MAX lignes consecutives. Deux formes sont
    indexees par fenetre : telle quelle, et privee de son prefixe de
    numerotation — parce que les titres de troisieme niveau sont imprimes
    sans numerotation.
    """
    index = collections.defaultdict(set)
    for fichier, imprimee, lignes in corpus.pages:
        for debut in range(len(lignes)):
            for taille in range(1, FENETRE_MAX + 1):
                if debut + taille > len(lignes):
                    break
                fenetre = ' '.join(lignes[debut:debut + taille])
                for forme in (reduit(fenetre),
                              reduit(PREFIXE_NUM.sub('', fenetre))):
                    if len(forme) >= 8:
                        index[forme].add((fichier, imprimee))
    return index


def index_fenetres_pistes(corpus):
    """-> [(fichier, page, texte_fenetre, forme_reduite)] pour le difflib.

    Limite aux fenetres qui peuvent etre un titre : une fenetre qui demarre
    en milieu de paragraphe n'a aucune raison d'etre proposee comme piste.
    On garde donc les fenetres dont la PREMIERE ligne commence par une
    majuscule, un guillemet ouvrant ou une numerotation.
    """
    debuts = re.compile(r'^(?:[A-ZÀ-ÖØ-Þ«"“(]|\d|[IVX]+\.)')
    sorties = []
    for fichier, imprimee, lignes in corpus.pages:
        for debut in range(len(lignes)):
            if not debuts.match(lignes[debut]):
                continue
            for taille in range(1, FENETRE_MAX + 1):
                if debut + taille > len(lignes):
                    break
                fenetre = ' '.join(lignes[debut:debut + taille])
                forme = reduit(PREFIXE_NUM.sub('', fenetre))
                if len(forme) >= 12:
                    sorties.append((fichier, imprimee, fenetre, forme))
    sorties.sort(key=lambda x: (x[1], x[0], x[2]))
    return sorties


def index_table_des_matieres(corpus):
    """-> {forme_reduite: [pages declarees]} lues dans la TDM imprimee.

    La TDM est reconstituee en un flux continu (les entrees y sont coupees
    par les sauts de ligne et les points de conduite), puis, pour chaque
    position d'un titre, on lit le PREMIER nombre isole qui suit dans une
    fenetre bornee. Corroboration seulement — cf. docstring.
    """
    flux, correspondance = [], []
    for imprimee, lignes in corpus.tdm:
        for ligne in lignes:
            if MARQUE_PAGE.fullmatch(ligne.strip()):
                continue
            for caractere in ligne + ' ':
                flux.append(caractere)
                correspondance.append(imprimee)
    texte = ''.join(flux)
    # Correspondance position_reduite -> position_texte, pour retrouver le
    # nombre qui suit une entree une fois celle-ci localisee sur la forme
    # reduite (immunisee aux points de conduite et aux coupures de ligne).
    # `frontieres[i]` dit si un caractere non alphanumerique separait ce
    # caractere reduit du precedent : sans cette marque, « Conclusion du
    # Chapitre I » se retrouverait DANS « Conclusion du Chapitre II » et la
    # TDM declarerait trois pages pour une seule entree.
    forme, positions, frontieres = [], [], []
    coupure = True
    for position, caractere in enumerate(texte):
        plie = re.sub(r'[^a-z0-9]', '', sans_accents(caractere).lower())
        if plie:
            for decalage, lettre in enumerate(plie):
                forme.append(lettre)
                positions.append(position)
                frontieres.append(coupure if decalage == 0 else False)
            coupure = False
        else:
            coupure = True
    return texte, ''.join(forme), positions, frontieres


def pages_declarees_tdm(tdm, cible):
    """Les pages que la TDM declare pour `cible` (forme reduite). Deterministe."""
    texte, forme, positions, frontieres = tdm
    if not cible or len(cible) < 8:
        return []
    trouvees, depart = [], 0
    while True:
        position = forme.find(cible, depart)
        if position < 0:
            break
        depart = position + 1
        fin_reduite = position + len(cible) - 1
        if fin_reduite >= len(positions):
            break
        debut_mot = position == 0 or frontieres[position]
        fin_mot = (fin_reduite + 1 >= len(forme)
                   or frontieres[fin_reduite + 1])
        if not (debut_mot and fin_mot):
            continue
        suite = texte[positions[fin_reduite] + 1:positions[fin_reduite] + 220]
        nombre = re.search(r'(?<![0-9])(\d{1,3})(?![0-9])', suite)
        if not nombre:
            continue
        # Le numero doit SUIVRE l'entree, separe d'elle par des points de
        # conduite et des espaces — pas etre celui d'une entree ulterieure.
        # Sans cette borne, « Entretiens » ramassait le numero d'une ligne
        # situee plusieurs entrees plus loin.
        intercale = re.sub(r'[.\s…·]', '', suite[:nombre.start()])
        if len(intercale) > 8:
            continue
        trouvees.append(int(nombre.group(1)))
    return sorted(set(trouvees))


# --------------------------------------------------------------------------
# le graphe
# --------------------------------------------------------------------------
def noeuds_de_section(graphe):
    """-> ([entites triees], {id: [noms de types]}). Sections ET chapitres."""
    nom_type = {t['id']: t.get('name') or t['id']
                for t in (graphe.get('types') or []) if t.get('id')}
    noeuds, types = [], {}
    for entite in graphe.get('entities') or []:
        eid = entite.get('id')
        if not eid:
            continue
        noms = sorted(nom_type.get(t, t) for t in (entite.get('types') or []))
        if any(n in TYPES_AUDITES for n in noms):
            noeuds.append(entite)
            types[eid] = noms
    noeuds.sort(key=lambda e: e['id'])
    return noeuds, types


def parents_de_section(graphe, types):
    """-> {id_enfant: id_parent} d'apres `section of` / `has section`.

    `chapter of` est volontairement ecarte : il relie une section a son
    chapitre, ce qui donnerait DEUX parents a la plupart des noeuds et
    rendrait la colonne `parent` illisible. Quand plusieurs parents de
    section subsistent, on prend le plus specifique (une section plutot
    qu'un chapitre), puis le plus petit id — determinisme avant tout.
    """
    par_nom = {}
    for rtype in (graphe.get('relation_types') or []):
        if rtype.get('id'):
            par_nom.setdefault(rtype.get('name') or rtype['id'], []).append(
                rtype['id'])
    ids_section_of = set(par_nom.get('section of', []))
    ids_has_section = set(par_nom.get('has section', []))
    candidats = collections.defaultdict(set)
    for relation in graphe.get('relations') or []:
        rtype = relation.get('type')
        if rtype in ids_section_of:
            candidats[relation.get('from')].add(relation.get('to'))
        elif rtype in ids_has_section:
            candidats[relation.get('to')].add(relation.get('from'))
    parents = {}
    for enfant, possibles in candidats.items():
        possibles = {p for p in possibles if p and p != enfant}
        if not possibles:
            continue
        sections = {p for p in possibles
                    if any(n in TYPES_SECTION for n in types.get(p, []))}
        retenus = sorted(sections or possibles)
        parents[enfant] = retenus[0]
    return parents


def cles_anterieures(chemin):
    """-> ({id: section_key}, chemin) lues dans un graphe ANTERIEUR, ou (None, None).

    Sert a une seule chose : etablir la cle qu'un noeud portait AVANT les
    renumerotations v100 et v106. Le graphe de reference est le plus ancien
    du depot (v96 au moment ou ce script est ecrit), c'est-a-dire anterieur
    aux deux migrations. Lecture seule, comme tout le reste.
    """
    if not chemin:
        return None, None
    graphe = lire_json(chemin, "graphe de reference historique")
    if not isinstance(graphe, dict) or not isinstance(
            graphe.get('entities'), list):
        echec_invocation(f"graphe historique sans liste d'entites : {chemin}")
    cles = {}
    for entite in graphe.get('entities') or []:
        eid = entite.get('id')
        attrs = entite.get('attributes')
        if not eid or not isinstance(attrs, dict):
            continue
        cle = valeur_texte(attrs.get('section_key'))
        if cle is not None and str(cle).strip():
            cles[eid] = str(cle).strip()
    return cles, chemin


def sections_sourcequote(chemin):
    """-> (ensemble de jetons de section cites par les 41 ops, nb d'ops lues).

    Le champ `target_section` melange plusieurs ecritures : « II.2 »,
    « II.3.2->II.3.1.b » (avant/apres renumerotation), « intro_C_2 |
    intro_C_2a » (plusieurs cibles). Tous les jetons sont retenus, des deux
    cotes d'une fleche : une section citee sous son ancienne cle est
    concernee autant que sous la nouvelle.
    """
    if not os.path.exists(chemin):
        return set(), 0
    jetons, lues = set(), 0
    try:
        with open(chemin, encoding='utf-8', newline='') as f:
            for ligne in csv.DictReader(f, delimiter=';'):
                lues += 1
                brut = (ligne.get('target_section') or '').strip()
                for morceau in re.split(r'[|]', brut):
                    for jeton in re.split(r'->', morceau):
                        jeton = jeton.strip()
                        if jeton:
                            jetons.add(jeton)
    except (OSError, UnicodeDecodeError, csv.Error) as err:
        echec_invocation(f"dossier SourceQuote illisible : {err}")
    return jetons, lues


def concernee(entite, cle, jetons):
    """La section est-elle visee par une des 41 ops ?

    Correspondance sur `section_key`, et a defaut sur le prefixe du nom :
    le lot designe « I.2.1b », qui n'est la cle d'aucun noeud mais le debut
    exact du nom du noeud 3ce505bc.
    """
    if cle and cle in jetons:
        return True
    nom = (entite.get('name') or '').strip()
    return any(nom.startswith(jeton + ' ') for jeton in jetons)


# --------------------------------------------------------------------------
# tri des cles de section
# --------------------------------------------------------------------------
_ROMAINS = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5}


def rang_de_cle(cle, nom, eid):
    """Cle de tri : les cles a ordre naturel d'abord, le reste en fin.

    Groupe 0 : « I.1.1.a » — chapitre romain, puis composantes numeriques,
               puis lettre. Groupe 1 : toute autre cle non vide, ordre
               alphabetique. Groupe 2 : les noeuds sans `section_key`.
    L'id termine chaque cle de tri : deux executions rendent le meme ordre.
    """
    if cle:
        morceaux = cle.split('.')
        if morceaux[0] in _ROMAINS:
            composantes = []
            for morceau in morceaux[1:]:
                if morceau.isdigit():
                    composantes.append((0, int(morceau), ''))
                else:
                    composantes.append((1, 0, morceau))
            return (0, _ROMAINS[morceaux[0]], composantes, '', '', eid)
        return (1, 0, [], cle, '', eid)
    return (2, 0, [], '', nom or '', eid)


# --------------------------------------------------------------------------
# audit
# --------------------------------------------------------------------------
def designe(entite):
    """Comment nommer un noeud dans une note : sa cle, sinon son id."""
    attrs = entite.get('attributes')
    cle = valeur_texte(attrs.get('section_key')) if isinstance(attrs, dict) \
        else None
    cle = str(cle).strip() if cle is not None else ''
    return cle or entite.get('id') or '?'


def nettoie(texte):
    """Un champ CSV : ';' -> ',', espaces reduits, jamais de saut de ligne."""
    return ' '.join(str(texte if texte is not None else '')
                    .replace(';', ',').split())


def audit(graphe, corpus, jetons_sq, seuil_piste, max_pistes, prefixe_min,
          cles_anciennes=None, chemin_ancien=None):
    """-> liste de dicts, un par noeud de section. Sans horodatage."""
    noeuds, types = noeuds_de_section(graphe)
    parents = parents_de_section(graphe, types)
    index = index_titres(corpus)
    fenetres = index_fenetres_pistes(corpus)
    tdm = index_table_des_matieres(corpus)

    par_id = {e['id']: e for e in noeuds}

    def attribut(entite, cle):
        attrs = entite.get('attributes')
        return valeur_texte(attrs.get(cle)) if isinstance(attrs, dict) else None

    lignes = []
    for entite in noeuds:
        eid = entite['id']
        cle = attribut(entite, 'section_key')
        cle = str(cle).strip() if cle is not None else ''
        nom = entite.get('name') or ''
        noms_types = types.get(eid, [])
        declaree = entier_ou_none(attribut(entite, 'page_start'))

        formes = denominations(entite)
        trouvees = set()
        for forme in formes:
            trouvees |= index.get(forme, set())
        pages = sorted({page for _, page in trouvees})

        piste_tdm = []
        for forme in formes:
            piste_tdm.extend(pages_declarees_tdm(tdm, forme))
        piste_tdm = sorted(set(piste_tdm))

        lignes.append({
            'entite': entite, 'entity_id': eid, 'section_key': cle,
            'nom': nom, 'types': noms_types, 'page_start': declaree,
            'formes': formes, 'localisations': sorted(trouvees),
            'pages_corps': pages, 'pages_tdm': piste_tdm,
            'parent_id': parents.get(eid),
        })

    # --- pistes difflib, seulement pour les titres non localises ----------
    for ligne in lignes:
        ligne['pistes'] = []
        ligne['pistes_prefixe'] = []
        if len(ligne['pages_corps']) == 1 or not ligne['formes']:
            continue
        # Toutes les denominations sont essayees, pas seulement la plus
        # longue : la plus longue est celle qui PORTE le prefixe de
        # numerotation, et le corps de la these imprime les titres de
        # troisieme niveau SANS numerotation. La comparer seule ratait
        # exactement les sections que ces pistes doivent eclairer.
        apparieur = difflib.SequenceMatcher()
        meilleures = {}
        for cible in ligne['formes']:
            apparieur.set_seq2(cible)
            for fichier, page, texte, forme in fenetres:
                rapport = len(forme) / len(cible)
                if not PISTE_LONGUEUR_MIN <= rapport <= PISTE_LONGUEUR_MAX:
                    continue
                apparieur.set_seq1(forme)
                if apparieur.real_quick_ratio() < seuil_piste:
                    continue
                if apparieur.quick_ratio() < seuil_piste:
                    continue
                ratio = apparieur.ratio()
                if ratio < seuil_piste:
                    continue
                courante = meilleures.get(page)
                if courante is None or ratio > courante[0]:
                    meilleures[page] = (round(ratio, 4), fichier, texte)
        ligne['pistes'] = sorted(
            ((page, ratio, fichier, texte)
             for page, (ratio, fichier, texte) in meilleures.items()),
            key=lambda x: (-x[1], x[0]))[:max_pistes]

        # Second filet, pour les titres que le graphe REFORMULE en cours de
        # route : « « Creuser au fond du terrier » : les recherches
        # documentaires » face au titre imprime, plus long, qui commence par
        # les memes mots. difflib les note trop bas ; un prefixe commun long
        # reste une piste utile — et rien de plus.
        if prefixe_min:
            partages = {}
            for cible in ligne['formes']:
                for fichier, page, texte, forme in fenetres:
                    if forme[:12] != cible[:12]:
                        continue
                    commun = 0
                    for a, b in zip(forme, cible):
                        if a != b:
                            break
                        commun += 1
                    if commun < prefixe_min:
                        continue
                    courante = partages.get(page)
                    if courante is None or commun > courante[0]:
                        partages[page] = (commun, fichier, texte)
            ligne['pistes_prefixe'] = sorted(
                ((page, commun, fichier, texte)
                 for page, (commun, fichier, texte) in partages.items()),
                key=lambda x: (-x[1], x[0]))[:max_pistes]

    # --- page imprimee retenue, statut, ecart -----------------------------
    page_par_id = {}
    for ligne in lignes:
        pages = ligne['pages_corps']
        ligne['page_verifiee'] = pages[0] if len(pages) == 1 else None
        if ligne['page_verifiee'] is not None:
            page_par_id[ligne['entity_id']] = ligne['page_verifiee']

    # Quelle section commence a la page N ? Sert a nommer, dans `note`, la
    # section dont un `page_start` errone porte en fait la page.
    section_a_la_page = collections.defaultdict(list)
    for ligne in lignes:
        if ligne['page_verifiee'] is not None:
            section_a_la_page[ligne['page_verifiee']].append(ligne)

    enfants = collections.defaultdict(list)
    for ligne in lignes:
        if ligne['parent_id']:
            enfants[ligne['parent_id']].append(ligne)

    # Deux noeuds qui revendiquent le MEME titre imprime : une reparation
    # mecanique leur donnerait la meme page sans que personne ne le voie.
    par_forme = collections.defaultdict(list)
    for ligne in lignes:
        for forme in ligne['formes']:
            par_forme[forme].append(ligne['entity_id'])
    for ligne in lignes:
        jumeaux = set()
        for forme in ligne['formes']:
            jumeaux |= {x for x in par_forme[forme]
                        if x != ligne['entity_id']}
        ligne['jumeaux'] = sorted(jumeaux)

    for ligne in lignes:
        est_chapitre = TYPE_CHAPITRE in ligne['types'] and not any(
            t in TYPES_SECTION for t in ligne['types'])
        if est_chapitre:
            ligne['statut'] = 'hors-perimetre'
        elif ligne['page_start'] is None:
            ligne['statut'] = 'absent'
        elif ligne['page_verifiee'] is None:
            ligne['statut'] = 'ambigu'
        elif ligne['page_start'] == ligne['page_verifiee']:
            ligne['statut'] = 'correct'
        else:
            ligne['statut'] = 'incoherent'
        if ligne['page_start'] is not None and ligne['page_verifiee'] is not None:
            ligne['ecart'] = ligne['page_start'] - ligne['page_verifiee']
        else:
            ligne['ecart'] = None

    # --- source de preuve --------------------------------------------------
    for ligne in lignes:
        if ligne['page_verifiee'] is not None:
            fichier = sorted(f for f, p in ligne['localisations']
                             if p == ligne['page_verifiee'])[0]
            ligne['source_preuve'] = f"{fichier} p.{ligne['page_verifiee']}"
        elif ligne['pages_corps']:
            lieux = ', '.join(f"{f} p.{p}" for f, p in ligne['localisations'])
            ligne['source_preuve'] = f"plusieurs occurrences exactes : {lieux}"
        else:
            ligne['source_preuve'] = TITRE_INTROUVABLE

    # --- notes -------------------------------------------------------------
    page_par_cle = {x['section_key']: x['page_verifiee'] for x in lignes
                    if x['section_key'] and x['page_verifiee'] is not None}
    for ligne in lignes:
        notes = []
        if ligne['statut'] == 'hors-perimetre':
            notes.append("noeud de type Chapter : la pagination d'un chapitre "
                         "repond a une autre logique (page de garde, non "
                         "premiere page de contenu) et aucun de ces noeuds ne "
                         "porte de page_start — hors perimetre du controle")

        # cause 1 : la cle du noeud a change de sens (v100 / v106) et le
        # page_start est reste celui de l'ANCIENNE cle. Preuve exigee : la
        # valeur declaree doit etre EXACTEMENT la page imprimee de la
        # section que designait cette ancienne cle.
        prouve_renumerotation = False
        if ligne['statut'] == 'incoherent' and cles_anciennes:
            ancienne = cles_anciennes.get(ligne['entity_id'])
            if ancienne and ancienne != ligne['section_key']:
                page_ancienne = page_par_cle.get(ancienne)
                if page_ancienne is not None \
                        and page_ancienne == ligne['page_start']:
                    prouve_renumerotation = True
                    notes.append(
                        "sequelle de renumerotation v100-v106 (la cle a "
                        f"change de sens) — PROUVE : ce noeud portait la cle "
                        f"« {ancienne} » dans "
                        f"{os.path.basename(chemin_ancien or '?')}, et son "
                        f"page_start {ligne['page_start']} est exactement la "
                        f"page imprimee de « {ancienne} » ; la valeur a suivi "
                        f"le noeud, pas la section — la page de "
                        f"« {ligne['section_key'] or ligne['entity_id']} » est "
                        f"p.{ligne['page_verifiee']}")

        # cause 2 : la valeur declaree est la page d'une AUTRE section
        if ligne['statut'] == 'incoherent' and not prouve_renumerotation:
            autres = [x for x in section_a_la_page.get(ligne['page_start'], [])
                      if x['entity_id'] != ligne['entity_id']]
            if autres:
                noms = ', '.join(
                    f"{x['section_key'] or x['entity_id']} (p.{x['page_verifiee']})"
                    for x in sorted(autres,
                                    key=lambda x: (x['section_key'],
                                                   x['entity_id'])))
                notes.append("erreur mecanique de pagination : la valeur "
                             f"declaree {ligne['page_start']} est la page "
                             f"imprimee d'une autre section — {noms}")
            else:
                notes.append("erreur mecanique de pagination : la valeur "
                             f"declaree {ligne['page_start']} n'est la page "
                             "de debut d'aucune section identifiee")

        # cause : numerotation imprimee != section_key
        if ligne['page_verifiee'] is not None and ligne['section_key']:
            imprimees = set()
            for fichier, page, texte, _ in fenetres:
                if page != ligne['page_verifiee']:
                    continue
                reduit_titre = reduit(PREFIXE_NUM.sub('', texte))
                if reduit_titre in ligne['formes']:
                    trouve = NUM_IMPRIMEE.match(texte)
                    if trouve:
                        imprimees.add(trouve.group(1).rstrip('.'))
            divergentes = sorted(n for n in imprimees
                                 if n.lower() != ligne['section_key'].lower())
            if divergentes:
                notes.append("numerotation IMPRIMEE differente de section_key : "
                             f"la these imprime « {', '.join(divergentes)} » "
                             f"la ou section_key vaut « {ligne['section_key']} » "
                             "— le script ne tranche pas laquelle a raison")

        # PIEGE 2 : parente anterieure = normal ; posterieure = suspect
        propres = [x for x in enfants.get(ligne['entity_id'], [])
                   if x['page_verifiee'] is not None]
        if ligne['page_start'] is not None and propres:
            premier = min(propres, key=lambda x: (x['page_verifiee'],
                                                  x['entity_id']))
            if ligne['page_start'] < premier['page_verifiee']:
                notes.append(
                    "parente legitimement anterieure : page_start "
                    f"{ligne['page_start']} precede son premier enfant "
                    f"{premier['section_key'] or premier['entity_id']} "
                    f"(p.{premier['page_verifiee']}) — ce n'est PAS une "
                    "anomalie")
            elif ligne['page_start'] > premier['page_verifiee']:
                notes.append(
                    "parente POSTERIEURE a son premier enfant "
                    f"{premier['section_key'] or premier['entity_id']} "
                    f"(p.{premier['page_verifiee']}) — suspect")

        if ligne['jumeaux']:
            noms = ', '.join(designe(par_id[j]) for j in ligne['jumeaux'])
            notes.append("titre partage avec un autre noeud du graphe "
                         f"({noms}) : une reparation mecanique leur donnerait "
                         "la meme page — arbitrage auteur")

        if ligne['statut'] == 'ambigu':
            if ligne['pages_corps']:
                notes.append("reellement ambigu : le titre est imprime a "
                             "l'identique sur plusieurs pages, aucune n'est "
                             "choisie ici")
            else:
                notes.append("reellement ambigu : aucun titre imprime ne "
                             "correspond exactement au libelle du graphe "
                             "(reformulation probable) — arbitrage auteur")

        for page, ratio, fichier, texte in ligne['pistes']:
            notes.append(f"PISTE (quasi-titre {ratio:.2f}) {fichier} p.{page} "
                         f": « {texte[:110]} » — NON RETENU comme preuve")
        for page, commun, fichier, texte in ligne['pistes_prefixe']:
            notes.append(f"PISTE (prefixe commun {commun} car.) {fichier} "
                         f"p.{page} : « {texte[:110]} » — NON RETENU comme "
                         "preuve")

        # Un `ambigu` dont toutes les pistes convergent vers le page_start
        # declare n'est pas dans le meme etat qu'un `ambigu` sans piste : le
        # dire evite de faire passer pour ouvert un cas qui ne l'est pas.
        if ligne['statut'] == 'ambigu':
            convergentes = ({p for p, _, _, _ in ligne['pistes']}
                            | {p for p, _, _, _ in ligne['pistes_prefixe']}
                            | set(ligne['pages_tdm']))
            if convergentes == {ligne['page_start']}:
                notes.append("pistes CONVERGENTES vers le page_start declare "
                             f"{ligne['page_start']} — rien a corriger si "
                             "l'auteur valide le rapprochement de titre")
            elif convergentes:
                notes.append("pistes DIVERGENTES du page_start declare "
                             f"{ligne['page_start']} : "
                             f"p.{', p.'.join(str(p) for p in sorted(convergentes))}")

        if ligne['pages_tdm']:
            if (ligne['page_verifiee'] is not None
                    and ligne['pages_tdm'] == [ligne['page_verifiee']]):
                notes.append("table des matieres imprimee : accord "
                             f"(p.{ligne['page_verifiee']})")
            else:
                notes.append("PISTE table des matieres imprimee : "
                             f"p.{', p.'.join(str(p) for p in ligne['pages_tdm'])}"
                             " — corroboration, jamais preuve")

        ligne['note'] = ' | '.join(notes)

    for ligne in lignes:
        parent = par_id.get(ligne['parent_id']) if ligne['parent_id'] else None
        if parent is None:
            ligne['parent'] = ''
            ligne['page_start_parent'] = None
        else:
            attrs = parent.get('attributes')
            cle_parent = (valeur_texte(attrs.get('section_key'))
                          if isinstance(attrs, dict) else None)
            ligne['parent'] = str(cle_parent).strip() if cle_parent \
                else (parent.get('name') or ligne['parent_id'])
            ligne['page_start_parent'] = entier_ou_none(
                valeur_texte(attrs.get('page_start'))
                if isinstance(attrs, dict) else None)
        ligne['concernee_sourcequote'] = 'oui' if concernee(
            ligne['entite'], ligne['section_key'], jetons_sq) else 'non'

    lignes.sort(key=lambda x: rang_de_cle(x['section_key'], x['nom'],
                                          x['entity_id']))
    return lignes


def en_lignes_csv(lignes):
    sorties = []
    for ligne in lignes:
        sorties.append({
            'section_key': nettoie(ligne['section_key']),
            'entity_id': nettoie(ligne['entity_id']),
            'nom_actuel': nettoie(ligne['nom']),
            'type': nettoie('|'.join(ligne['types'])),
            'page_start_actuel': '' if ligne['page_start'] is None
                                 else str(ligne['page_start']),
            'page_imprimee_verifiee': '' if ligne['page_verifiee'] is None
                                      else str(ligne['page_verifiee']),
            'ecart': '' if ligne['ecart'] is None else str(ligne['ecart']),
            'statut': ligne['statut'],
            'source_preuve': nettoie(ligne['source_preuve']),
            'parent': nettoie(ligne['parent']),
            'page_start_parent': '' if ligne['page_start_parent'] is None
                                 else str(ligne['page_start_parent']),
            'concernee_sourcequote': ligne['concernee_sourcequote'],
            'note': nettoie(ligne['note']),
        })
    return sorties


def ecrit_csv(chemin, sorties):
    dossier = os.path.dirname(os.path.abspath(chemin))
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    with open(chemin, 'w', encoding='utf-8', newline='') as f:
        graveur = csv.DictWriter(f, fieldnames=list(COLONNES), delimiter=';',
                                 lineterminator='\n')
        graveur.writeheader()
        graveur.writerows(sorties)


def lit_csv(chemin):
    if not os.path.exists(chemin):
        echec_invocation(f"CSV de diagnostic introuvable : {chemin}")
    try:
        with open(chemin, encoding='utf-8', newline='') as f:
            lecteur = csv.DictReader(f, delimiter=';')
            manquantes = set(COLONNES) - set(lecteur.fieldnames or [])
            if manquantes:
                echec_invocation(f"CSV de diagnostic sans les colonnes "
                                 f"{sorted(manquantes)} : {chemin}")
            return list(lecteur)
    except (OSError, UnicodeDecodeError, csv.Error) as err:
        echec_invocation(f"CSV de diagnostic illisible : {err}")


# --------------------------------------------------------------------------
# rapports
# --------------------------------------------------------------------------
def rapport_calibration(corpus):
    print("=== CALIBRATION (pages IMPRIMEES, jamais des offsets) ===")
    for fichier in PDF_CORPS + (PDF_TDM,):
        etendue = corpus.etendues.get(fichier)
        marque = '  (exclu de la recherche de titres)' if fichier == PDF_TDM \
            else ''
        if etendue:
            print(f"  {fichier:32s} p.{etendue[0]}-{etendue[1]}{marque}")
        else:
            print(f"  {fichier:32s} AUCUNE page numerotee{marque}")
    trous = corpus.trous()
    print(f"  suite imprimee : {'continue, sans trou' if not trous else 'TROUS ' + str(trous)}")
    if corpus.anomalies:
        print(f"  pages sans numero imprime exploitable : "
              f"{len(corpus.anomalies)} (ecartees de l'index)")
        for fichier, offset, nombre, motif in corpus.anomalies:
            print(f"    {fichier} offset {offset} : {motif}")
    else:
        print("  pages sans numero imprime exploitable : aucune")
    print()


def rapport(lignes, chemin_graphe, jetons_sq, ops_sq):
    par_statut = collections.Counter(x['statut'] for x in lignes)
    print(f"graphe  : {os.path.relpath(chemin_graphe, REPO)}")
    print(f"noeuds  : {len(lignes)} noeuds de section audites")
    print(f"          {sum(1 for x in lignes if x['page_start'] is not None)} "
          "portent un page_start")
    print("\n=== REPARTITION PAR STATUT ===")
    for statut in STATUTS:
        print(f"  {statut:15s} {par_statut.get(statut, 0):3d}")

    incoherents = [x for x in lignes if x['statut'] == 'incoherent']
    print(f"\n=== INCOHERENCES ({len(incoherents)}) ===")
    if not incoherents:
        print("  (aucune)")
    for x in incoherents:
        print(f"  {x['section_key'] or x['entity_id']:12s} declare "
              f"p.{x['page_start']:<4d} imprime p.{x['page_verifiee']:<4d} "
              f"ecart {x['ecart']:+d}   [{x['source_preuve']}]")

    causes = collections.Counter()
    for x in incoherents:
        if 'PROUVE' in x['note']:
            causes['sequelle de renumerotation v100-v106 (PROUVE)'] += 1
        elif 'erreur mecanique' in x['note']:
            causes['erreur mecanique de pagination'] += 1
        else:
            causes['sans cause etablie'] += 1
    if causes:
        print("  --- causes")
        for cause, nombre in sorted(causes.items()):
            print(f"  {nombre:3d}  {cause}")

    ambigus = [x for x in lignes if x['statut'] == 'ambigu']
    print(f"\n=== AMBIGUS ({len(ambigus)}) ===")
    if not ambigus:
        print("  (aucun)")
    for x in ambigus:
        print(f"  {x['section_key'] or x['entity_id']:12s} declare "
              f"p.{x['page_start']} — {x['source_preuve']}")
        if x['note']:
            print(f"      {x['note'][:300]}")

    accords = desaccords = sans = 0
    for x in lignes:
        if x['page_verifiee'] is None:
            continue
        if not x['pages_tdm']:
            sans += 1
        elif x['pages_tdm'] == [x['page_verifiee']]:
            accords += 1
        else:
            desaccords += 1
    print("\n=== CORROBORATION PAR LA TABLE DES MATIERES IMPRIMEE ===")
    print(f"  accord {accords} / desaccord {desaccords} / non declare {sans} "
          f"(sur {accords + desaccords + sans} titres localises)")
    for x in lignes:
        if x['page_verifiee'] is not None and x['pages_tdm'] \
                and x['pages_tdm'] != [x['page_verifiee']]:
            print(f"    {x['section_key'] or x['entity_id']:12s} corps "
                  f"p.{x['page_verifiee']} / TDM "
                  f"p.{', p.'.join(str(p) for p in x['pages_tdm'])}")

    concernees = [x for x in lignes if x['concernee_sourcequote'] == 'oui']
    print(f"\n=== SECTIONS VISEES PAR LES {ops_sq} OPS SOURCEQUOTE "
          f"({len(concernees)} noeuds) ===")
    for x in concernees:
        print(f"  {x['section_key'] or x['entity_id']:12s} {x['statut']:12s} "
              f"declare {x['page_start'] if x['page_start'] is not None else '-'} "
              f"/ imprime {x['page_verifiee'] if x['page_verifiee'] is not None else '-'}")
    cles = {x['section_key'] for x in lignes if x['section_key']}
    noms = [x['nom'] for x in lignes]
    orphelins = sorted(j for j in jetons_sq if j not in cles
                       and not any(n.startswith(j + ' ') for n in noms))
    if orphelins:
        print(f"  jetons du lot SourceQuote sans noeud correspondant "
              f"({len(orphelins)}) : {', '.join(orphelins)}")
    print()


def controle(lignes):
    """`--check` : 1 des qu'un page_start diverge d'une page imprimee etablie."""
    divergents = [x for x in lignes if x['statut'] == 'incoherent']
    for x in divergents:
        print(f"DIVERGENCE {x['section_key'] or x['entity_id']:12s} "
              f"page_start={x['page_start']} page imprimee="
              f"{x['page_verifiee']} (ecart {x['ecart']:+d}) "
              f"[{x['source_preuve']}]", file=sys.stderr)
    if divergents:
        print(f"ECHEC (donnees) : {len(divergents)} page_start divergent de la "
              "page imprimee verifiee.", file=sys.stderr)
        return CODE_DIVERGENCE
    print(f"OK : aucun page_start ne diverge de sa page imprimee verifiee "
          f"({sum(1 for x in lignes if x['statut'] == 'correct')} verifies, "
          f"{sum(1 for x in lignes if x['statut'] == 'ambigu')} non etablis).")
    return 0


def controle_sur_csv(graphe, chemin_csv):
    """Repli sans pypdf : le controle s'appuie sur la preuve ENREGISTREE."""
    print(f"pypdf absent — repli sur la preuve enregistree : "
          f"{os.path.relpath(chemin_csv, REPO)}", file=sys.stderr)
    attendues = {}
    for ligne in lit_csv(chemin_csv):
        page = entier_ou_none(ligne.get('page_imprimee_verifiee'))
        if page is not None:
            attendues[(ligne.get('entity_id') or '').strip()] = (
                page, (ligne.get('section_key') or '').strip())
    noeuds, types = noeuds_de_section(graphe)
    noeuds.sort(key=lambda e: rang_de_cle(designe(e) if
                                          designe(e) != e['id'] else '',
                                          e.get('name') or '', e['id']))
    divergents = 0
    verifies = 0
    for entite in noeuds:
        if TYPE_CHAPITRE in types.get(entite['id'], []) and not any(
                t in TYPES_SECTION for t in types.get(entite['id'], [])):
            continue
        attrs = entite.get('attributes')
        declaree = entier_ou_none(valeur_texte(attrs.get('page_start'))
                                  if isinstance(attrs, dict) else None)
        attendue = attendues.get(entite['id'])
        if declaree is None or attendue is None:
            continue
        verifies += 1
        if declaree != attendue[0]:
            divergents += 1
            print(f"DIVERGENCE {attendue[1] or entite['id']:12s} "
                  f"page_start={declaree} page imprimee={attendue[0]} "
                  f"(ecart {declaree - attendue[0]:+d}) [CSV enregistre]",
                  file=sys.stderr)
    if divergents:
        print(f"ECHEC (donnees) : {divergents} page_start divergent de la page "
              "imprimee enregistree.", file=sys.stderr)
        return CODE_DIVERGENCE
    print(f"OK : aucun page_start ne diverge ({verifies} compares contre la "
          "preuve enregistree, non re-mesuree).")
    return 0


# --------------------------------------------------------------------------
def main(argv=None):
    p = argparse.ArgumentParser(
        description="Audite les `page_start` des noeuds de section du graphe "
                    "GRC-20 contre la page ou leur titre est IMPRIME dans les "
                    "PDF canoniques de la these. Lecture seule du graphe : ce "
                    "script n'ecrit jamais un graphe, une carte ou un patch. "
                    "Sans --csv, il n'ecrit rien du tout.",
        epilog="Codes de sortie : 0 = l'audit a tourne (des incoherences "
               "restent un resultat) ; 1 = --check a trouve au moins une "
               "divergence ; 2 = erreur d'invocation. La page imprimee n'est "
               "JAMAIS deduite d'un offset de fichier : chaque page est "
               "calibree sur sa marque « — NN — ». Une parente qui commence "
               "avant ses enfants n'est pas une incoherence : le verdict ne "
               "compare que le page_start d'une section a la page ou SON "
               "titre est imprime. Le dossier SourceQuote ne sert qu'a "
               "remplir la colonne concernee_sourcequote, jamais a choisir "
               "une page.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--graph', default=None, metavar='FICHIER',
                   help="graphe audite (defaut : le plus recent du depot)")
    p.add_argument('--csv', nargs='?', const=CSV_AUTO, default=None,
                   metavar='CHEMIN',
                   help="ECRIT le CSV de diagnostic (';'-separe). Sans "
                        "valeur, le nom est DERIVE de la version du graphe "
                        "audite (docs/audits/data/"
                        "section-page-start-diagnostic-vNNN.csv), pour qu'un "
                        "audit de v111 n'ecrase pas la preuve v110. Omettre "
                        "l'option = aucune ecriture")
    p.add_argument('--check', action='store_true',
                   help="ne rapporte que les divergences et sort en code 1 "
                        "s'il y en a — le controle qui devra rester vert "
                        "apres une reparation")
    p.add_argument('--pdf-dir', default=DOSSIER_PDF, metavar='DOSSIER',
                   help="dossier des PDF canoniques (defaut : "
                        f"{os.path.relpath(DOSSIER_PDF, REPO)})")
    p.add_argument('--historique', default=None, metavar='FICHIER',
                   help="graphe ANTERIEUR aux renumerotations v100/v106, lu "
                        "en lecture seule pour etablir la cle qu'un noeud "
                        "portait avant (defaut : le plus ancien graphe du "
                        "depot). Sert uniquement a PROUVER la cause d'un "
                        "ecart, jamais a choisir une page")
    p.add_argument('--sans-historique', action='store_true',
                   help="n'ouvre aucun graphe anterieur : les causes se "
                        "limitent alors a ce que le graphe courant montre")
    p.add_argument('--sourcequote', default=SOURCEQUOTE_DEFAUT,
                   metavar='FICHIER',
                   help="dossier de verification SourceQuote, lu UNIQUEMENT "
                        "pour la colonne concernee_sourcequote "
                        f"(defaut : {os.path.relpath(SOURCEQUOTE_DEFAUT, REPO)})")
    p.add_argument('--piste-seuil', type=float, default=PISTE_SEUIL_DEFAUT,
                   metavar='R',
                   help="ratio difflib minimal d'un quasi-titre propose comme "
                        "PISTE dans `note` (defaut : %(default)s). Une piste "
                        "n'est jamais une preuve")
    p.add_argument('--piste-prefixe', type=int, default=PISTE_PREFIXE_DEFAUT,
                   metavar='N',
                   help="longueur minimale, en caracteres reduits, du prefixe "
                        "commun qui fait proposer un titre imprime comme "
                        "PISTE quand difflib ne le note pas assez haut "
                        "(defaut : %(default)s ; 0 = desactive)")
    p.add_argument('--piste-max', type=int, default=PISTE_MAX_DEFAUT,
                   metavar='N',
                   help="nombre maximal de pistes par section "
                        "(defaut : %(default)s ; 0 = aucune)")
    args = p.parse_args(argv)

    if args.piste_max < 0:
        echec_invocation("--piste-max ne peut pas etre negatif")
    if args.piste_prefixe < 0:
        echec_invocation("--piste-prefixe ne peut pas etre negatif")
    if not 0.0 < args.piste_seuil <= 1.0:
        echec_invocation("--piste-seuil doit etre dans ]0, 1]")

    chemin_graphe = args.graph or graphe_le_plus_recent()
    if not chemin_graphe:
        echec_invocation("aucun graphe grc20-these-mael-rolland-v*.json dans "
                         "le depot (et aucun --graph fourni)")
    graphe = lire_json(chemin_graphe, 'graphe audite')
    if not isinstance(graphe, dict) or not isinstance(
            graphe.get('entities'), list):
        echec_invocation(f"graphe sans liste d'entites : {chemin_graphe}")

    # la sentinelle CSV_AUTO se resout maintenant : la version du graphe
    # audite est connue (arbitrage de robustesse, revue hostile prise 3)
    chemin_csv_defaut = csv_defaut(chemin_graphe)
    if args.csv == CSV_AUTO:
        args.csv = chemin_csv_defaut

    pypdf = importe_pypdf()
    if pypdf is None:
        if args.check and not args.csv:
            return controle_sur_csv(graphe, chemin_csv_defaut)
        echec_invocation(
            "pypdf est indispensable pour etablir les pages imprimees et il "
            "est absent (pip install pypdf). Repli disponible : `--check` "
            "seul, qui compare le graphe a la preuve deja enregistree dans "
            f"{os.path.relpath(chemin_csv_defaut, REPO)}")

    corpus = Corpus()
    corpus.charge(pypdf, args.pdf_dir)
    if not corpus.pages:
        echec_invocation(f"aucune page numerotee dans {args.pdf_dir}")

    jetons_sq, ops_sq = (set(), 0) if args.check else \
        sections_sourcequote(args.sourcequote)

    if args.sans_historique:
        cles_anciennes, chemin_ancien = None, None
    else:
        anciens = [f for f in graphes_tries() if f != chemin_graphe]
        cles_anciennes, chemin_ancien = cles_anterieures(
            args.historique or (anciens[0] if anciens else None))

    lignes = audit(graphe, corpus, jetons_sq, args.piste_seuil,
                   args.piste_max, args.piste_prefixe,
                   cles_anciennes, chemin_ancien)

    if args.check:
        return controle(lignes)

    rapport_calibration(corpus)
    if chemin_ancien:
        print("=== REFERENCE HISTORIQUE (cles d'avant les renumerotations) ===")
        print(f"  {os.path.relpath(chemin_ancien, REPO)} — lue en lecture "
              "seule, pour prouver une cause, jamais pour choisir une page\n")
    rapport(lignes, chemin_graphe, jetons_sq, ops_sq)

    if args.csv:
        ecrit_csv(args.csv, en_lignes_csv(lignes))
        print(f"CSV de diagnostic ecrit : {os.path.relpath(args.csv, REPO)} "
              f"({len(lignes)} lignes)")
    else:
        print("(aucune ecriture — passer --csv pour produire le CSV de "
              "diagnostic)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
