# PLAN FRONT 10b : Composants UI et Dashboard de Planification

**Objectif :** Développer l'interface graphique du tableau de bord de planification (Dashboard) en exploitant le hook `usePlanning` et les données mockées (réalisés lors du plan 10a). L'objectif est d'afficher visuellement la grille des shifts pour chaque agent ainsi que l'analyse de couverture quotidienne.

---

## 1. Analyse DDD et Stratégie (Strategic Domain Design)

Pour l'interface utilisateur (UI), nous allons suivre une architecture de type **Container / Presentational Components** (Composants Intelligents / Composants Stupides) afin de garantir une séparation claire des responsabilités au sein de notre couche de Présentation.

### Bounded Contexts Front-end (Couche Présentation)

1.  **Dumb Components (Composants de Présentation Purs) :**
    - **Responsabilité :** Afficher des données visuelles et émettre des événements utilisateurs. Ils n'ont pas conscience de l'origine des données (API ou Mocks) et ne gèrent pas d'états asynchrones complexes.
    - **Modèles concernés :** 
      - `PlanningTable` : Reçoit une liste de `AgentPlanning` et affiche une grille (Lignes = Agents, Colonnes = Jours, Cellules = Shifts).
      - `CoverageSummary` : Reçoit une liste de `DayCoverage` et affiche un résumé visuel (ex: jauges ou pastilles de couleur) signalant si l'effectif cible est atteint (gap de 0), en déficit (gap négatif) ou en surplus (gap positif).

2.  **Smart Components (Containers / Pages) :**
    - **Responsabilité :** Orchestrer l'application, récupérer les données (via les hooks du domaine), gérer les états globaux (Chargement, Erreur) et fournir les données aux composants enfants de présentation.
    - **Modèles concernés :**
      - `PlanningDashboard` : La vue principale qui appelle le hook `usePlanning`, affiche un "Loading spinner" pendant le chargement, ou un message d'erreur si l'appel échoue, puis transmet les données récupérées à `PlanningTable` et `CoverageSummary`.

### Context Map

- **[Hook] `usePlanning` ➔ [Container] `PlanningDashboard` ➔ [Dumb Components] (`PlanningTable`, `CoverageSummary`)**

---

## 2. Plan de Développement (Séquence de Commits TDD)

Voici le plan ordonné pour le développeur React (`react-developer`). Chaque étape doit faire l'objet d'un cycle complet : **Test (React Testing Library) ➔ Code ➔ Refactor ➔ Commit ➔ Pause**.

1.  `test(ui): Add rendering tests for CoverageSummary component`
    *   *Objectif :* Créer les tests pour vérifier que le composant de couverture s'affiche correctement selon les différentes valeurs de gap (couleurs différentes pour surplus, déficit et cible atteinte).
2.  `feat(ui): Implement CoverageSummary component`
    *   *Objectif :* Créer `src/components/CoverageSummary.tsx` avec un design simple (ex: des badges ou des barres) basé sur le contrat `DayCoverage[]`.
3.  `test(ui): Add tests for PlanningTable component`
    *   *Objectif :* Tester que le tableau affiche bien la liste des agents, les dates en en-têtes, et les shifts correspondants (repos vs travail) basés sur les données mockées.
4.  `feat(ui): Implement PlanningTable component`
    *   *Objectif :* Créer `src/components/PlanningTable.tsx` qui prend la prop `AgentPlanning[]` pour générer une grille visuelle.
5.  `test(ui): Create tests for PlanningDashboard smart component`
    *   *Objectif :* Tester que le composant gère bien les 3 états de notre hook : 1. Affiche "Loading" initialement, 2. Affiche un message d'erreur si `error` est non-null, 3. Affiche les composants enfants quand `data` est présent. (Nécessite de mocker le hook `usePlanning`).
6.  `feat(ui): Implement PlanningDashboard composing Table and Coverage`
    *   *Objectif :* Créer `src/pages/PlanningDashboard.tsx` qui instancie le hook `usePlanning` et distribue les props à `PlanningTable` et `CoverageSummary`.
7.  `feat(core): Update App component to render PlanningDashboard`
    *   *Objectif :* Modifier `src/App.tsx` pour remplacer le contenu par défaut de Vite par notre `PlanningDashboard`. (Pas de test spécifique obligatoire ici si c'est juste de l'assemblage basique).
