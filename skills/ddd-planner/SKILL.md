---
name: ddd-planner
description: "Analyse un besoin métier et conçoit une architecture DDD stratégique (Strategic Domain Design). Définit les Bounded Contexts et produit un plan de développement sous forme de commits atomiques."
---

# DDD Planner Skill

Ce skill guide l'agent dans l'analyse d'un besoin métier et la conception d'une architecture logicielle basée sur le Domain-Driven Design (DDD).

## Mission

Analyser le besoin initial et concevoir une SDD (Strategic Domain Design).

## Workflow

1.  **Analyser la demande de l'utilisateur :** Comprendre le domaine métier, les objectifs et les contraintes. Poser des questions de clarification si nécessaire pour établir un langage omniprésent (Ubiquitous Language).
2.  **Identifier les Bounded Contexts :** Découper le domaine en contextes bornés clairs, chacun avec ses propres modèles et responsabilités.
3.  **Définir la Context Map :** Décrire les relations entre les différents Bounded Contexts (ex: Upstream/Downstream, Shared Kernel, Anti-Corruption Layer).
4.  **Produire le plan de développement :**
    *   Créer une liste séquentielle et détaillée de commits atomiques.
    *   Chaque commit doit représenter une étape logique et testable du développement.
    *   Le plan doit être suffisamment clair pour être implémenté par un autre agent (le `ddd-developer`).

## Livrables

-   Une description claire des Bounded Contexts identifiés.
-   Une Context Map (peut être sous forme de texte ou de diagramme simple).
-   Une liste ordonnée de messages de commit qui serviront de plan de développement.

**Exemple de plan de commits :**

1.  `feat(core): Setup initial Django project structure for DDD`
2.  `feat(identity): Define User and Role aggregates within the Identity & Access Bounded Context`
3.  `test(identity): Add unit tests for User aggregate business rules`
4.  `feat(catalog): Implement Product entity and Catalog Bounded Context`
5.  `test(catalog): Write integration tests for adding a product to the catalog`
