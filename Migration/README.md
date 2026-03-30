# Story Mode Implementation Pack

Ce dossier contient un pack complet à déposer dans le repo pour qu’un agent de code puisse lire un cahier des charges structuré, détaillé et cohérent avant d’implémenter un système de micro-récits dans le graphe.

## Fichiers

- `01_AGENT_MASTER_BRIEF.md` : brief principal à donner à l’agent
- `02_TECHNICAL_SPEC.md` : contrat technique détaillé
- `03_STORY_CONTENT_SPEC.md` : contenu narratif des 4 récits prioritaires
- `04_ACCEPTANCE_AND_QA.md` : critères d’acceptation et checklist de test
- `story-presets.seed.mjs` : exemple de registre central de récits, prêt à adapter

## Usage recommandé

1. Déposer l’ensemble du dossier dans le repo, par exemple dans `docs/story-mode/`.
2. Demander à l’agent de lire d’abord `01_AGENT_MASTER_BRIEF.md` puis `02_TECHNICAL_SPEC.md`.
3. Lui demander d’utiliser `03_STORY_CONTENT_SPEC.md` comme source de vérité narrative.
4. Lui imposer de vérifier `04_ACCEPTANCE_AND_QA.md` avant de considérer la tâche comme terminée.
5. Lui signaler que `story-presets.seed.mjs` est un point de départ, pas nécessairement la version finale exacte.

## Intention

Le but n’est pas de créer un deuxième système parallèle, mais un surplomb narratif réutilisable du graphe existant.
