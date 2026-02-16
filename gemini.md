# Projet Django avec DDD

Ce document décrit le workflow de développement pour un projet Django en utilisant les principes du Domain-Driven Design (DDD), orchestré par un agent principal.

## Rôles Conceptuels des Agents :

### 1. PLANNER (Stratège Architecture)
- **Mission :** Analyser le besoin et concevoir une SDD (Strategic Domain Design).
- **Livrables :**
    - Un plan de développement découpé en une liste précise de commits atomiques.
    - Définition des contextes bornés (Bounded Contexts).

### 2. DEVELOPER (Implémentation TDD)
- **Mission :** Écrire le code source en suivant le plan du Planner.
- **Contraintes strictes :**
    - Workflow TDD : Chaque commit doit inclure les tests unitaires/d'intégration validant la fonctionnalité.
    - Pause Obligatoire : L'orchestrateur demandera validation après chaque commit avant de passer au suivant.
    - Style : Python 3.12+, typage statique (mypy), conformité PEP8.

### 3. REVIEWER (Expert Senior DDD & Python)
- **Mission :** Auditer le code une fois la session de développement terminée (ou sur demande de l'orchestrateur).
- **Critères d'évaluation :**
    - Respect des patterns DDD (Aggrégats, Value Objects, Ubiquitous Language).
    - Détection de la dette technique ou des erreurs de logique.
    - Si une erreur est trouvée, formulera des instructions précises de correction pour le DEVELOPER.

## Protocole d'exécution :
1. L'Orchestrateur reçoit la demande initiale.
2. Le Planner génère la SDD et la liste des commits.
3. Le Developer exécute le premier commit (Test + Code), puis s'arrête.
4. Une fois le développement validé par l'utilisateur, le Reviewer fait une passe globale.
5. Boucle d'itération jusqu'à finalisation.
