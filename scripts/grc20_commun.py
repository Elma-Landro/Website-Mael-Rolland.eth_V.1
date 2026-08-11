#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utilitaires partages par les scripts GRC-20. N'ecrit rien, n'a aucun effet.

Ce module nait d'un constat de relecture : `sans_accents`, `normalise` et
`graphe_le_plus_recent` etaient reecrits dans plusieurs scripts. La mise en
commun n'a pas seulement supprime des lignes, elle a revele deux divergences
qui comptent.

**Deux normalisations, pas une.** Les copies de `normalise` ne faisaient pas
la meme chose : l'une se contentait de minuscules + apostrophe droite,
l'autre supprimait en plus toute ponctuation et normalisait les espaces.
Deux fonctions distinctes sous un meme nom. Les fusionner aurait change le
comportement de l'une des deux en silence. Elles sont donc gardees toutes
les deux, sous des noms qui disent ce qu'elles font :
`normalise_doux` et `normalise_appariement`.

**Une selection de graphe fragile.** Une copie de `graphe_le_plus_recent`
appelait `.group(1)` sans verifier le motif et `max()` sans verifier que la
liste etait non vide : un fichier `grc20-these-mael-rolland-vX.json` mal
nomme la faisait planter par `AttributeError`, et un depot sans graphe par
`ValueError`. C'est la version defensive qui est retenue ici.
"""
import glob
import os
import re
import unicodedata

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MOTIF_GRAPHE = 'grc20-these-mael-rolland-v*.json'
_NUM_VERSION = re.compile(r'-v(\d+)\.json$')


def sans_accents(s):
    """« émergence » -> « emergence ». Identique dans les trois copies d'origine."""
    s = unicodedata.normalize('NFD', s or '')
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')


def normalise_doux(s):
    """Minuscules, sans accents, apostrophe droite. La ponctuation est GARDEE.

    Sert aux comparaisons de libelles ou la ponctuation porte du sens —
    `check_anchoring` compare ainsi des noms d'entites.
    """
    return sans_accents(s).lower().replace('’', "'").strip()


def normalise_appariement(s):
    """Comme `normalise_doux`, mais toute ponctuation devient espace.

    Sert a apparier des titres dont la ponctuation varie d'une source a
    l'autre — « CM : boucs emissaires » face a « CM, boucs emissaires ».
    Deux graphies differentes doivent y donner la meme chaine.
    """
    s = sans_accents(s).lower().replace('’', "'")
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return ' '.join(s.split())


def numero_de_version(chemin):
    """-> int, ou None si le nom ne porte pas de numero exploitable."""
    m = _NUM_VERSION.search(chemin)
    return int(m.group(1)) if m else None


def graphes_tries(repo=REPO):
    """Les graphes du depot, du plus ancien au plus recent.

    Les fichiers dont le nom ne porte pas de numero sont ecartes plutot que
    de faire planter le tri.
    """
    fichiers = glob.glob(os.path.join(repo, MOTIF_GRAPHE))
    numerotes = [(numero_de_version(f), f) for f in fichiers]
    return [f for n, f in sorted(numerotes) if n is not None]


def graphe_le_plus_recent(repo=REPO):
    """Le plus grand numero de version present, ou None si le depot n'en a aucun."""
    tries = graphes_tries(repo)
    return tries[-1] if tries else None


# Les sections de la these ne portent pas toutes le meme type. 73 sont des
# `ThesisSection` ; une seule — III.3, « Une gouvernance publique
# d'exception » — porte `ChapterSection`, type dont elle est l'unique
# occurrence du graphe. Tout outil qui ne regarde que `ThesisSection` la tient
# pour absente : `make_section_creation_patch.py` s'appretait a la recreer, a
# cote d'un noeud existant et deja relie.
#
# On ne retype rien ici — ce serait un arbitrage, pas une correction — mais
# aucun outil ne doit plus raisonner sur un seul des deux noms.
TYPES_SECTION = ('ThesisSection', 'ChapterSection')


def est_section(entite, nom_type):
    """`nom_type` : {id de type -> nom}. Vrai si l'entite est une section."""
    noms = [nom_type.get(t, t) for t in (entite.get('types') or [])]
    return any(t in noms for t in TYPES_SECTION)


# --- Ops qu'aucun applicateur du depot ne consomme -------------------------
#
# Deux scripts posaient la meme question sans se parler :
# `preflight_candidate_patches.py` balayait dynamiquement scripts/ pour
# CREATE_ENTITY puis, a l'identique, pour ADD_RELATION ; et
# `build_patch_queue_inventory.py` portait une liste STATIQUE des memes types.
# Deux notions du meme fait, dont une qui ne se met pas a jour toute seule :
# le jour ou un applicateur est ecrit, le balayage le voit et la liste
# statique, non — la file continuerait a dire « bloque faute d'applicateur »
# sur un patch devenu applicable.
#
# La question est donc posee ici, une fois, et par MESURE plutot que par
# declaration. Limite assumee, heritee du balayage d'origine : le critere est
# litteral (un simple commentaire nommant le type suffit a le declencher) et
# ne voit pas un applicateur au dispatch purement structurel. Le constat du
# jour a ete verifie a la main en plus du balayage.
OPS_SANS_APPLICATEUR_CONNU = ('CREATE_ENTITY', 'ADD_RELATION')


def applicateurs_par_op(repo=REPO, types=OPS_SANS_APPLICATEUR_CONNU):
    """-> {type d'op: [applicateurs qui le nomment]}, tri stable.

    Vide pour un type = aucun applicateur ne le consomme aujourd'hui. Le jour
    ou l'un d'eux le traitera, les controles qui s'appuient dessus changeront
    seuls, sans qu'aucune liste ait a etre mise a jour."""
    textes = {}
    for motif in (os.path.join(repo, 'scripts', 'make_*.py'),
                  os.path.join(repo, 'scripts', '*.mjs')):
        for chemin in sorted(glob.glob(motif)):
            try:
                with open(chemin, encoding='utf-8') as f:
                    textes[os.path.basename(chemin)] = f.read()
            except OSError:
                continue
    return {t: [nom for nom, texte in sorted(textes.items()) if t in texte]
            for t in types}
