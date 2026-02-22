---
name: react-developer
description: "Implémente le code source front-end en suivant un plan de commits. Applique un workflow TDD strict, écrit du code React avec TypeScript, et attend une validation après chaque commit."
---

# React Developer Skill

Ce skill guide l'agent dans l'écriture du code source front-end (React/TypeScript) en suivant un plan de développement pré-établi, avec un focus sur la qualité, le Test-Driven Development (TDD) et l'architecture (DDD ou Clean Architecture adaptée au front).

## Mission

Écrire le code source front-end en suivant un plan de commits détaillé.

## Workflow et Contraintes Strictes

1.  **Exécuter un seul commit à la fois :** Prendre la prochaine étape du plan de développement. Ne jamais exécuter plus d'une étape à la fois.
2.  **Appliquer le TDD (Test-Driven Development) :**
    *   **Écrire le test en premier :** Créer les tests (unitaires avec Vitest/Jest, ou composants avec React Testing Library) qui échouent initialement mais qui valident la fonctionnalité décrite dans le commit.
    *   **Écrire le code :** Implémenter le code source (composants, hooks, services, domain) nécessaire pour faire passer les tests.
    *   **Refactoriser :** Améliorer la structure du code si nécessaire, tout en s'assurant que les tests continuent de passer.
3.  **Respecter les standards de style :**
    *   Langage : TypeScript avec React (FC, Hooks).
    *   Typage : Typage strict requis. Éviter `any`.
    *   Style : Assurer la conformité avec ESLint/Prettier si présents dans le projet. Respecter les principes d'architecture si appliqués (isolation du domaine, UI "dumb").
4.  **Pause Obligatoire :** Après avoir réalisé le commit (tests + code), **arrêter impérativement**. Attendre la validation de l'orchestrateur (l'utilisateur) avant de passer au commit suivant du plan.

## Livrable par étape

-   Un seul commit Git contenant à la fois les tests et le code d'implémentation correspondant à une étape du plan.
