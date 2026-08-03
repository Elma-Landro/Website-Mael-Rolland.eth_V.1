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
