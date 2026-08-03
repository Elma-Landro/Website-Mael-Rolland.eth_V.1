---
name: grc20-visual-coherence
description: >
  Vérifie ce que le site de Maël Rolland donne réellement à voir : qu'une entrée
  du sommaire charge la section qu'elle annonce, que les références par nom du
  runtime résolvent, qu'aucun panneau ne se vide en silence. À invoquer après
  tout changement du graphe GRC-20, de graphe.html, lecteur.html,
  story-presets.mjs, graphe.story-helpers.js ou narrative-anchors.json — et
  avant toute PR qui les touche. Exige d'ouvrir les pages dans un navigateur :
  un contrôle statique ne voit pas ce que voit le lecteur. Contient la procédure
  de test locale, CDN bloqués compris.
---

# Visual-Coherence-Reviewer — ouvrir la page, pas seulement le fichier

**Ne conclus jamais sans avoir ouvert la page.** Les quatre défauts qui ont
justifié cette instance étaient tous invisibles à la lecture du code :
14 entrées de sommaire chargeaient la mauvaise section ; 3 195 relations
étaient injoignables ; 4 références d'alias étaient mortes, dont 2 que le
contrôle d'ancrage ne voyait pas ; et `crisis.html` appelait `data.filter` sur
une variable inexistante, sur une page publiée.

## Monter le banc de test

Les CDN sont bloqués dans cet environnement. **Sans contournement,
`graphe.html` n'initialise pas son graphe et aucun compteur du sommaire n'est
calculé** — on croit la page cassée alors qu'elle ne l'est pas.

```bash
python3 -m http.server 8899 >/dev/null 2>&1 &
cd /tmp && npm install playwright cytoscape@3.28.1 dagre@0.8.5 \
                       cytoscape-dagre@2.5.0 --no-save --silent
```

Puis, dans le script Playwright, sers les bibliothèques depuis le disque :

```js
await p.route('**/*', r => {
  const u = r.request().url();
  for (const [n, c] of Object.entries(LOCAUX))
    if (u.endsWith(n)) return r.fulfill({ contentType: 'application/javascript',
                                          body: fs.readFileSync(c, 'utf8') });
  if (/^https:\/\/fonts\./.test(u)) return r.fulfill({ status: 200, contentType: 'text/css', body: '' });
  return r.continue();
});
```

Chromium est préinstallé : `executablePath: '/opt/pw-browsers/chromium'`.
Ne lance **jamais** `playwright install`.

Relève systématiquement les `pageerror` et les `console.error`.

## Les contrôles

**1. Chaque entrée du sommaire résout-elle ?**
`graphe.html` porte 48 `data-section-key`. Chacune doit correspondre à un nœud
du graphe — via `grc20_commun.est_section`, **pas seulement `ThesisSection`** :
`III.3` est un `ChapterSection` et serait tenue pour absente.

**2. Chaque entrée affiche-t-elle quelque chose ?**
Le sommaire suit la table des matières de la thèse, qui s'arrête au niveau 2 :
`II.1.1` y figure, `II.1.1.a` non. Le contenu vit souvent dans les rangs
subordonnés. Les deux pages agrègent la section et ses enfants — `lecteur.html`
reconstitue les parentes au chargement, `graphe.html` par `sectionNodeIdsFor()`.
Vérifie les compteurs :

```js
[...document.querySelectorAll('.story-toc li[data-section-key]')]
  .map(li => [li.dataset.sectionKey, li.querySelector('.toc-count')?.textContent || '—'])
```

**3. Les références par nom résolvent-elles ?**
`scripts/check_anchoring.py` n'en couvre qu'une partie. La seule méthode
fiable : comparer **tous** les noms qui changent entre vN et vN+1 à **tous** les
fichiers du runtime.

```python
renommes = {n105[i]: n106[i] for i in n105 if i in n106 and n105[i] != n106[i]}
for f in ('story-presets.mjs', 'graphe.story-helpers.js', 'narrative-anchors.json',
          'graphe.html', 'lecteur.html', 'section_entities_map.json'):
    hits = [(a, b) for a, b in renommes.items() if a and a in open(f, encoding='utf-8').read()]
```

Ces tables sont indexées **par nom d'entité** : tout renommage les casse.
`narrative-anchors.json` se reconstruit (`node narrative-anchors-build.mjs`) ;
les tables d'alias se corrigent à la main.

**4. Le contrôle d'ancrage régresse-t-il ?**
`python3 scripts/check_anchoring.py` — il n'échoue que sur les problèmes
**absents** de `docs/audits/data/anchoring-baseline.json`. Une régression
acceptée s'inscrit dans la baseline **avec son motif**, jamais en silence.

## Ce que tu ne dois pas conclure

- **Qu'un panneau à 12 nœuds et 0 lien est un défaut.** Mesuré sur 53 sections :
  c'est un trait de la sélection top-12 par TF-IDF, qui retient des entités
  distinctives donc peu reliées. Une hypothèse contraire a été testée et
  démentie.
- **Qu'un compte est « meilleur » sans avoir mesuré l'avant.** Un « après » sans
  « avant » relevé n'est pas un résultat.
- **Que les densités affichées sont fiables.** Le classement repose sur
  `occurrence_count`, dont 44 % des nœuds affichés portent un poids qui n'est
  pas le leur (`docs/audits/grc20-ancrage-poids-mandataires-v1.md`). Signale-le
  quand c'est en jeu ; ne le corrige pas — c'est un arbitrage ouvert.

## Sortie

```
CONTRÔLE     ce qui est vérifié
AVANT        le chiffre relevé, avec la commande
APRÈS        le chiffre relevé, avec la commande
NAVIGATEUR   ce qui a été ouvert, pageerrors comprises
VERDICT      régression / amélioration / inchangé
```

## Interdits

- Ne modifie le runtime que sur mission explicite.
- Ne conclus rien d'une page qui n'a pas chargé ses bibliothèques.
- Ne « modernise » pas le design : la police 8 bits, la palette néon et le rendu
  pixelisé sont voulus.
- N'inscris rien dans la baseline sans en écrire le motif.
