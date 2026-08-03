/**
 * Lecture des clés de section de la thèse — partagée par graphe.html et
 * lecteur.html.
 *
 * Les deux pages doivent s'accorder sur ce que « contient » une section : le
 * sommaire s'arrête au niveau 2 de la table des matières (« II.1.1 » y figure,
 * « II.1.1.a » non), alors que le contenu vit sur les rangs subordonnés. Une
 * section montre donc ce que portent ses descendants.
 *
 * Elles ne s'accordaient pas. Sur 16 des 48 entrées du sommaire, `graphe.html`
 * agrégeait tous les descendants tandis que `lecteur.html` s'arrêtait aux
 * enfants directs, et sautait toute parente ayant du contenu propre — `I.2.2`
 * affichait ses 265 entités en taisant les 142 de `I.2.2.b`. Deux
 * implémentations de la même règle, c'était deux réponses. D'où ce fichier :
 * la règle est écrite une fois.
 *
 * DEUX SÉPARATEURS. Les chapitres numérotent au point (`I.2.2`, `II.1.1.a`),
 * l'introduction au souligné (`intro_A`, `intro_B_1a`). N'en tester qu'un
 * laissait 22 sections de l'introduction hors de portée de ses 5 entrées de
 * sommaire. Les clés de la conclusion (`conclu_aceph`) sont des feuilles.
 */
(function attachSectionHelpers(globalObj) {
  const SEPARATEURS = ['.', '_'];

  /** `cle` est-elle un descendant strict de `parente` ? */
  function estDescendant(cle, parente) {
    if (!cle || !parente || cle === parente) return false;
    return SEPARATEURS.some(s => cle.indexOf(parente + s) === 0);
  }

  /**
   * Les ancêtres d'une clé, du plus proche au plus lointain.
   * « II.1.1.a » -> [« II.1.1 », « II.1 »] ; « intro_B_1a » -> [« intro_B »].
   *
   * On s'arrête dès qu'un ancêtre ne porte plus de séparateur : « II » et
   * « intro » ne sont pas des sections de la thèse, seulement le début d'une
   * clé. Les inclure ferait agréger tout un chapitre sous une clé qui n'existe
   * pas.
   */
  function ancetres(cle) {
    const out = [];
    let c = cle || '';
    for (;;) {
      let i = -1;
      for (const s of SEPARATEURS) i = Math.max(i, c.lastIndexOf(s));
      if (i <= 0) break;
      c = c.slice(0, i);
      if (!SEPARATEURS.some(s => c.indexOf(s) !== -1)) break;
      out.push(c);
    }
    return out;
  }

  /**
   * -> { parente: [descendants triés] }, en UNE passe sur les clés.
   *
   * Les parentes sortent des clés elles-mêmes, et non de la liste fournie :
   * la plupart n'y figurent pas, et c'est précisément le problème — « II.1.1 »
   * n'a pas d'entrée dans la carte d'ancrage alors que « II.1.1.a » en a une.
   * Chercher les parentes parmi les seules clés présentes les manquerait
   * toutes.
   */
  function arbreDescendants(cles) {
    const arbre = {};
    for (const cle of cles) {
      for (const a of ancetres(cle)) (arbre[a] || (arbre[a] = [])).push(cle);
    }
    for (const a of Object.keys(arbre)) arbre[a].sort();
    return arbre;
  }

  globalObj.GRC20Sections = { estDescendant, ancetres, arbreDescendants };
})(typeof window !== 'undefined' ? window : globalThis);
