# PLAN FRONT 10a : Architecture et Mocks pour l'Intégration API

**Objectif :** Analyser le besoin d'intégration avec le backend (Plan 10), définir l'architecture front-end correspondante, et établir un plan de développement robuste basé sur des mocks pour commencer le travail d'interface utilisateur en isolation.

---

## 1. Analyse DDD et Stratégie (Strategic Domain Design)

Pour l'application React, nous allons structurer le code en séparant le domaine métier de l'infrastructure réseau.

### Bounded Contexts Front-end

1.  **Planning Domain (Domaine Métier) :**
    - **Responsabilité :** Représenter la logique métier et les entités au sein du navigateur (Agents, Shifts, Couverture).
    - **Modèles :** Interfaces TypeScript strictes (`AgentPlanning`, `PlannedDay`, `Shift`, `DayCoverage`). Ces modèles doivent refléter fidèlement le contrat défini par le backend.
2.  **API / Infrastructure Layer (Anti-Corruption Layer) :**
    - **Responsabilité :** Gérer la communication avec l'extérieur. Agit comme un rempart (ACL) pour traduire les réponses HTTP brutes en objets du domaine front-end, si nécessaire.
    - **Implémentation :** Services simulant (pour cette phase) des appels asynchrones au réseau (`planningService.ts`), et fournissant les données factices (`planningData.ts`).
3.  **Application / Presentation (UI State) :**
    - **Responsabilité :** Gérer l'état de l'interface (chargement, erreur, affichage des données) et orchestrer les appels aux services.
    - **Implémentation :** Hooks personnalisés React (ex: `usePlanning.ts`) qui consomment l'infrastructure.

### Context Map

- **Backend API (Django) ➔ [Conformiste / Customer-Supplier] ➔ Frontend API Service ➔ Frontend Domain ➔ UI Components**
  *Pour l'instant, le Frontend API Service est "bouchonné" (Mocked).*

---

## 2. Plan de Développement (Séquence de Commits TDD)

Voici le plan ordonné pour le développeur React (`react-developer`). Chaque étape doit faire l'objet d'un cycle complet : **Test ➔ Code ➔ Refactor ➔ Commit ➔ Pause**.

1.  `test(planning): Add type validation tests for domain models`
    *   *Objectif :* Mettre en place les tests vérifiant que de futurs objets respectent bien la structure attendue.
2.  `feat(planning): Define TypeScript domain interfaces for Planning and Coverage`
    *   *Objectif :* Créer `src/types/planning.ts` avec les interfaces `Shift`, `PlannedDay`, `AgentPlanning`, `DayCoverage`.
3.  `test(mocks): Add tests validating mock data structure against domain interfaces`
    *   *Objectif :* S'assurer que les données factices que nous allons créer ne dérivent pas de nos types stricts.
4.  `feat(mocks): Implement static mock data matching backend API contract`
    *   *Objectif :* Créer `src/mocks/planningData.ts` avec des données réalistes (agents : Alice, Bob, Charlie...; cycles 12h 2-2; couverture correspondante).
5.  `test(services): Write tests for simulated async API service calls`
    *   *Objectif :* Tester que le service retourne bien des promesses résolues avec les données mockées après un délai.
6.  `feat(services): Create mock API service functions with simulated latency`
    *   *Objectif :* Créer `src/services/planningService.ts` exposant `fetchFullPlanning` et `fetchCoverageAnalysis` en utilisant `setTimeout`.
7.  `test(hooks): Create unit tests for usePlanning custom hook`
    *   *Objectif :* Tester le hook en mockant le service pour vérifier les changements d'état (`isLoading: true -> false`, `error: null`, `data: [...]`).
8.  `feat(hooks): Implement usePlanning hook to expose data, loading, and error states`
    *   *Objectif :* Créer `src/hooks/usePlanning.ts` pour encapsuler l'orchestration de la récupération des données de planification.
