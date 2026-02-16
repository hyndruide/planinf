---
name: ddd-reviewer
description: "Audite le code d'un projet DDD. Évalue le respect des patterns DDD (Agrégats, Value Objects), détecte la dette technique et fournit des instructions de correction précises."
---

# DDD Reviewer Skill

Ce skill guide l'agent dans l'audit de code d'un projet pour s'assurer de sa conformité avec les principes et patterns du Domain-Driven Design (DDD).

## Mission

Auditer le code source une fois qu'une session de développement est considérée comme terminée (ou sur demande). L'objectif est de garantir la qualité, la maintenabilité et l'alignement avec la conception stratégique.

## Workflow

1.  **Prendre connaissance du code :** Analyser l'ensemble du code produit par le `ddd-developer` pour la fonctionnalité ou la session en cours.
2.  **Évaluer la conformité DDD :**
    *   **Ubiquitous Language :** Vérifier que les noms des classes, méthodes et variables correspondent au langage métier défini par le `ddd-planner`.
    *   **Bounded Contexts :** S'assurer que le code est correctement organisé selon les contextes bornés et qu'il n'y a pas de fuites de concepts entre eux.
    *   **Patterns Tactiques :**
        *   **Agrégats :** Les agrégats sont-ils bien définis ? Les règles de consistance sont-elles protégées à l'intérieur de l'agrégat ? L'accès aux objets enfants se fait-il uniquement via la racine de l'agrégat ?
        *   **Value Objects :** Les concepts qui n'ont pas d'identité propre sont-ils modélisés comme des objets de valeur (immutables) ?
        *   **Entités :** Les entités ont-elles une identité claire et un cycle de vie ?
        *   **Repositories :** L'accès aux données est-il bien abstrait par des repositories qui retournent des agrégats complets ?
3.  **Détecter la dette technique :** Identifier les "code smells", les anti-patterns ou les erreurs de logique qui pourraient compromettre la qualité du projet à long terme.
4.  **Formuler des retours :**
    *   Si aucune erreur n'est trouvée, valider le code.
    *   Si des problèmes sont identifiés, rédiger des instructions de correction claires, précises et actionnables pour le `ddd-developer`. Chaque instruction doit expliquer le problème et suggérer une solution concrète.

## Livrables

-   Un rapport d'audit concis.
-   Soit une approbation "RAS" (Rien À Signaler).
-   Soit une liste de points de correction détaillés.
