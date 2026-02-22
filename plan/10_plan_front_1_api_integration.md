# PLAN FRONT 01 : Intégration API et Structure de Base

**Objectif :** Établir la connexion avec le backend Django et préparer les services de données pour l'application React. Ce document sert de contrat d'interface (API) pour le développement du frontend.

---

## 1. Description de l'API Backend

Le backend expose actuellement deux endpoints principaux sous forme d'API REST (JSON) pour alimenter le tableau de bord de planification.

### A. Endpoint : Matrice de Planning Global (Full View)

Cet endpoint permet de récupérer le planning projeté pour l'ensemble des agents sur une période donnée (généralement 12 semaines).

- **URL :** `/api/v1/planning/full-view/`
- **Méthode :** `GET`
- **Paramètres de requête (Query Params) :**
  - `start_date` (Requis) : Date de début de la projection au format `YYYY-MM-DD`.
  - `weeks` (Optionnel, défaut: 12) : Nombre de semaines à projeter.

- **Format de réponse (JSON) :** Une liste d'objets représentant chaque agent et son planning quotidien.
  ```json
  [
    {
      "agent_id": "uuid-agent-1",
      "nom": "Alice",
      "planning": [
        {
          "date": "2026-02-16",
          "shift": {
            "type": "WORK",
            "duration": 12
          }
        },
        {
          "date": "2026-02-17",
          "shift": {
            "type": "REST",
            "duration": 0
          }
        }
        // ... (suite des jours sur la période demandée)
      ]
    },
    // ... (suite des agents)
  ]
  ```

### B. Endpoint : Analyse de Couverture (Santé du Planning)

Cet endpoint fournit les données pour afficher si l'effectif cible est atteint chaque jour (le "gap" ou écart).

- **URL :** `/api/v1/coverage/analysis/`
- **Méthode :** `GET`
- **Paramètres de requête (Query Params) :**
  - `start_date` (Requis) : Date de début de l'analyse au format `YYYY-MM-DD`.
  - `end_date` (Requis) : Date de fin de l'analyse au format `YYYY-MM-DD`.

- **Format de réponse (JSON) :** Une liste d'objets détaillant la couverture jour par jour.
  ```json
  [
    {
      "date": "2026-02-16",
      "present_count": 3,
      "required_count": 2,
      "gap": 1  // Surplus de 1 agent
    },
    {
      "date": "2026-02-17",
      "present_count": 1,
      "required_count": 2,
      "gap": -1 // Déficit de 1 agent
    }
    // ...
  ]
  ```

### C. Endpoints CRUD (Création, Lecture, Modification, Suppression)

Le backend expose des ViewSets complets pour administrer les ressources de base. Ces endpoints supportent les méthodes standards : `GET` (liste/détail), `POST` (création), `PUT`/`PATCH` (modification), `DELETE` (suppression).

1.  **Gestion des Agents :**
    - **URL :** `/api/v1/resources/agents/`
    - **Payload POST type :** `{"nom": "Alice", "quotite": 1.0, "date_debut_cycle": "2026-01-01", "est_surnumeraire": false}`

2.  **Gestion des Trames :**
    - **URL :** `/api/v1/patterns/trames/`
    - **Payload POST type :** `{"nom": "Cycle 12h", "duree_cycle_jours": 14, "sequence_data": [{"type": "WORK", "duration": 12}, {"type": "REST", "duration": 0}]}`

3.  **Gestion des Besoins Quotidiens (Effectif cible) :**
    - **URL :** `/api/v1/coverage/requirements/`
    - **Payload POST type :** `{"day_of_week": 0, "required_count": 5}` *(Note: `day_of_week` va de 0=Lundi à 6=Dimanche)*

4.  **Gestion des Affectations (Lien manuel Agent <-> Trame) :**
    - **URL :** `/api/v1/planning/affectations/`

5.  **Gestion des Absences :**
    - **URL :** `/api/v1/planning/absences/`

### D. Endpoint : Génération Automatique (Solveur OR-Tools)

Cet endpoint déclenche l'intelligence artificielle pour générer automatiquement les trames et les affectations.

- **URL :** `/api/v1/solver/generate/`
- **Méthode :** `POST`
- **Payload (JSON) :**
  ```json
  {
    "agent_ids": ["uuid-1", "uuid-2", "uuid-3"],
    "politique_id": "uuid-politique",
    "duree_cycle": 84,
    "date_debut": "2026-01-01"
  }
  ```
- **Réponses :**
  - `201 Created` : "Schedule generated successfully"
  - `422 Unprocessable Entity` : "No feasible solution found" (Impossible de respecter les règles avec ces effectifs)

---

## 2. Tâches de Développement Frontend (React)

### Tâche 1 : Configuration des appels API
- **Action :** Créer un dossier `src/services/` ou `src/api/`.
- **Action :** Implémenter un client HTTP (par exemple avec `axios` ou `fetch`) pointant vers l'URL de base du backend (ex: `http://localhost:8000`).
- **Action :** Créer les fonctions `fetchFullPlanning(startDate, weeks)` et `fetchCoverage(startDate, endDate)`.

### Tâche 2 : Définition des Types (TypeScript)
- **Action :** Créer un fichier `src/types/index.ts`.
- **Action :** Définir les interfaces TypeScript correspondant aux JSON ci-dessus (`Agent`, `PlannedDay`, `Shift`, `DayCoverage`).

### Tâche 3 : Mocking (Optionnel mais recommandé)
- **Action :** En attendant que le backend soit connecté et rempli de données pertinentes, créer un fichier `src/mocks/apiMock.ts` qui renvoie des données statiques au même format pour pouvoir commencer à développer l'UI (Matrice et Graphique) immédiatement.
