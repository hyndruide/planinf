# PLAN FRONT 10e : Formulaire Dynamique et Couverture Trame

**Objectif :** Rendre le formulaire de génération de planning dynamique en y intégrant la sélection des agents (via cases à cocher) et la sélection multiple des politiques de conformité. De plus, conformément au cahier des charges initial (Notion), il faut afficher un outil permettant de vérifier la "couverture pour une trame donnée" (le besoin).

---

## 1. Analyse DDD (Frontend & UX)

Suite à la relecture du document de conception ("Projet ben", "USM unit schedule Manager"), voici les points clés extraits pour la couche Présentation (UI) :

1.  **Dashboard Configuration (Input) :**
    - L'écran 1 est dédié à la configuration : "Grille de saisie du besoin (7 colonnes pour les jours de la semaine)".
    - Il inclut la sélection des agents.
2.  **Visualiseur de Trame (Output) :**
    - L'écran 2 montre la matrice (déjà implémentée) ET un "Indicateur de santé (Check de couverture : est-ce que le besoin est rempli chaque jour ?)".

**Problème Actuel :**
Le besoin (Coverage Requirement) est actuellement codé en dur (`required_count = 2`) dans nos mocks et notre tableau. Le Notion spécifie un "Need (Le Besoin) : Valeur d'entrée (input) fixant le nombre d'agents nécessaires par jour (ex: Lundi = 5)".

**Action (Stratégie UI) :**
Nous allons faire évoluer notre `GeneratePlanningForm` pour qu'il ne soit pas qu'un bouton "Générer", mais un véritable "Dashboard Configuration" (Écran 1 du Notion). Il va intégrer :
- La liste des agents (cases à cocher).
- La liste des politiques (multi-select).
- *Nouveau :* Une grille de saisie des besoins (Need) pour définir la couverture cible *avant* la génération.

### Bounded Contexts & Modèles

- **Planning Domain (Types) :**
  - Ajout des types `Agent` et `Politique`.
  - Modification de `GeneratePlanningPayload` pour inclure les `politique_ids` (tableau) et potentiellement les besoins quotidiens modifiés (bien que le backend gère ça via les endpoints `/requirements/`, on va s'assurer que le Front les manipule).

---

## 2. Plan de Développement (Séquence de Commits TDD)

Voici le plan pour le développeur React (`react-developer`).

1.  `feat(types): Update Domain types for Agents, Politiques and Requirements`
    *   *Objectif :* Dans `types/planning.ts`, ajouter `Agent` (id, nom), `Politique` (id, nom), et `DailyRequirementInput` (jour, nombre). Mettre à jour `GeneratePlanningPayload` avec `politique_ids: string[]`.
2.  `feat(services): Add mock data and fetchers for configuration options`
    *   *Objectif :* Dans `planningData.ts` et `planningService.ts`, simuler la récupération de la liste des Agents existants, des Politiques existantes, et de la configuration des besoins quotidiens (Lundi à Dimanche).
3.  `feat(hooks): Create useConfiguration hook to load form dependencies`
    *   *Objectif :* Créer un hook `useConfiguration.ts` qui charge asynchronement la liste des agents, des politiques et des besoins par défaut pour pré-remplir le formulaire.
4.  `feat(ui): Refactor GeneratePlanningForm with checkboxes and multi-select`
    *   *Objectif :* Modifier le formulaire pour utiliser les données du hook `useConfiguration`. Remplacer l'input texte par des `<input type="checkbox">` pour la liste des agents. Remplacer le `<select>` simple par une sélection multiple pour les politiques.
5.  `feat(ui): Add Daily Requirement grid to Configuration Form`
    *   *Objectif :* Ajouter une section "Saisie du besoin" dans le formulaire avec 7 champs (Lundi à Dimanche) permettant au manager de définir l'objectif de couverture (Écran 1 du Notion). Mettre à jour le payload de soumission.
