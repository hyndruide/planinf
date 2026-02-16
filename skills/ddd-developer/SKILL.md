---
name: ddd-developer
description: "Implémente le code source en suivant un plan de commits fourni par le ddd-planner. Applique un workflow TDD strict, écrit du code Python 3.12+ typé, et attend une validation après chaque commit."
---

# DDD Developer Skill

Ce skill guide l'agent dans l'écriture du code source en suivant un plan de développement pré-établi, avec un focus sur la qualité et le Test-Driven Development (TDD).

## Mission

Écrire le code source en suivant le plan de commits fourni par le `ddd-planner`.

## Workflow et Contraintes Strictes

1.  **Exécuter un seul commit à la fois :** Prendre la prochaine étape du plan de développement fourni par le `ddd-planner`. Ne jamais exécuter plus d'une étape à la fois.
2.  **Appliquer le TDD (Test-Driven Development) :**
    *   **Écrire le test en premier :** Créer les tests (unitaires ou d'intégration) qui échouent initialement mais qui valident la fonctionnalité décrite dans le commit.
    *   **Écrire le code :** Implémenter le code source nécessaire pour faire passer les tests.
    *   **Refactoriser :** Améliorer la structure du code si nécessaire, tout en s'assurant que les tests continuent de passer.
3.  **Respecter les standards de style :**
    *   Langage : Python 3.12+
    *   Typage : Utiliser le typage statique partout (`mypy`).
    *   Style : Assurer la conformité avec PEP8.
4.  **Pause Obligatoire :** Après avoir réalisé le commit (tests + code), **arrêter impérativement**. Attendre la validation de l'orchestrateur (l'utilisateur) avant de passer au commit suivant du plan.

## Livrable par étape

-   Un seul commit Git contenant à la fois les tests et le code d'implémentation correspondant à une étape du plan.
