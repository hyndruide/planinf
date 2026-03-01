# PLAN 17 : Spécifications et Plan d'Intégration pour l'Équipe Frontend (React)

## 1. Contexte et Objectifs
L'objectif de l'application **Planinf** est de remplacer un processus complexe de gestion de plannings hospitaliers actuellement géré sur un fichier Excel lourd (avec macros VBA). Le frontend React doit offrir une interface fluide, intuitive et réactive, destinée principalement aux Cadres de Santé et aux administrateurs RH.

Nous avons développé un Backend robuste (en Python/Django) qui intègre un moteur de génération automatique (OR-Tools), un moteur de conformité légale, et un calculateur de balances horaires. Le Frontend actuel (basé sur Vite + React + TypeScript) implémente déjà une version basique et mockée de la "Vue Globale du Planning" et du "Formulaire de Génération". 

L'objectif de ce plan est de guider l'équipe Frontend pour brancher l'application sur les vraies APIs Backend et enrichir l'UI avec les nouvelles fonctionnalités (Vérificateur, Compteurs RH, Saisie des Besoins en volume, Indicateurs de Sous-Effectifs).

---

## 2. État des Lieux du Frontend Actuel

*   **Stack :** React 19, TypeScript, Vite, Vitest pour les tests.
*   **Composants existants :**
    *   `PlanningDashboard.tsx` : Conteneur principal.
    *   `PlanningTable.tsx` : Affiche la grille des agents, leurs shifts (icônes `Briefcase`/`Coffee`), et le calcul de couverture (Gap) en dessous.
    *   `GeneratePlanningForm.tsx` : Formulaire permettant de choisir les agents, les politiques et de configurer les besoins quotidiens.
*   **Hooks & Services :**
    *   `usePlanning.ts` / `useConfiguration.ts` : Gèrent l'état (actuellement branchés sur des mocks locaux).
    *   `planningService.ts` : Simule les appels API avec des `setTimeout`.

---

## 3. Plan d'Intégration et Nouvelles Fonctionnalités

L'équipe Frontend devra suivre ces étapes pour intégrer le travail du Backend :

### Étape A : Branchement sur l'API Réelle (Démockage)
Actuellement, `src/services/planningService.ts` renvoie des données statiques (`mockAgentPlanning`). 
1.  **Remplacer les requêtes mockées** par de vrais appels `fetch` (ou via `axios`) vers le backend Django tournant sur `http://localhost:8000`.
2.  **Endpoints à connecter :**
    *   `fetchFullPlanning` -> `GET /api/v1/planning/full-view/?start_date=...&weeks=...`
    *   `fetchCoverageAnalysis` -> `GET /api/v1/demand/analysis/?start_date=...&end_date=...`
    *   `fetchAllAgents` -> `GET /api/v1/resources/agents/`
    *   `fetchAllPolitiques` -> `GET /api/v1/compliance/politiques/`
    *   `generatePlanning` -> `POST /api/v1/solver/generate/`
    *   `updateDailyRequirements` -> `POST /api/v1/coverage/requirements/bulk/` (Utilisé lors de la soumission du formulaire de génération si les besoins ont été modifiés).

### Étape B : Amélioration Visuelle de la Couverture (Soft Constraints)
Le solveur backend a été mis à jour (Plan 18) pour accepter de générer des plannings même si l'effectif cible ne peut pas être atteint (Soft Constraints).
1.  **Mise à jour de `PlanningTable.tsx` (Footer de couverture) :**
    *   Si le `gap` est négatif (ex: Effectif Insuffisant, on a 4 agents mais on en voulait 5), la case doit être très visible (rouge/orange) avec un texte clair comme `Insuffisant (-1)`.
    *   Si le `gap` est positif (Surnuméraire), la case doit être d'une autre couleur d'alerte (ex: bleu/jaune) avec `Surnuméraire (+1)`.
    *   Si `gap === 0`, vert (`OK`).

### Étape C : Intégration du "Vérificateur" (Audit de Conformité)
Le backend dispose d'un service d'audit capable d'indiquer si un planning respecte la loi jour par jour.
1.  **Nouveau Service API :** Créer une fonction `fetchPlanningAudit` appelant `GET /api/v1/compliance/audit/?agent_id=...&start_date=...&end_date=...`.
2.  **Mise à jour de `usePlanning.ts` :** Intégrer l'appel à l'audit lors du chargement du planning.
3.  **Mise à jour de `PlanningTable.tsx` :**
    *   Pour chaque cellule de shift (`td`), vérifier si l'audit retourne `is_compliant === false` pour cette date.
    *   Si non conforme, appliquer un style d'alerte (ex: bordure rouge épaisse, fond légèrement teinté, icône "Attention").
    *   Ajouter un infobulle (Tooltip) affichant le `message` d'erreur remonté par l'API (ex: *"Dépassement du maximum hebdomadaire glissant"*).

### Étape D : Tableau de Bord Analytique (Compteurs & ETP)
Le backend calcule les balances horaires et les ETP (Équivalents Temps Plein). Il faut créer une nouvelle vue pour ces rapports.
1.  **Nouveau Composant `HRDashboard.tsx` :**
    *   À afficher dans un onglet séparé ou en bas de page.
2.  **Balances Horaires par Agent :**
    *   Appel API : `GET /api/v1/time/balance/{agent_id}/?start_date=...&end_date=...`
    *   Afficher un tableau récapitulatif pour chaque agent : *Heures Travaillées, Heures Dues, Balance (Crédit/Débit), RTT Acquis*.
3.  **Rapport ETP du Service :**
    *   Appel API : `GET /api/v1/planning/reports/fte/?start_date=...&end_date=...`
    *   Afficher des indicateurs visuels (KPI Cards) : *ETP Cible, ETP Réel, Total Heures de Nuit*.

### Étape E : Saisie des Desiderata (Absences)
Avant de lancer le solveur, les utilisateurs doivent pouvoir poser des absences (qui seront respectées comme contraintes fortes par le solveur).
1.  **Interface de saisie :** Ajouter un moyen (ex: clic droit sur une cellule vide du `PlanningTable` ou un bouton dédié) pour ajouter une absence (CA, Maladie, etc.) pour un agent à des dates précises.
2.  **API liée :** `POST /api/v1/planning/absences/`
3.  **Visualisation :** Dans le `PlanningTable`, afficher l'absence (ex: fond grisé, texte "CA").

### Étape F : Édition Manuelle (Drag & Drop / Modal) - *Bonus*
Dans le fichier Excel, l'utilisateur pouvait modifier manuellement une case.
1.  Permettre de cliquer sur une cellule de `PlanningTable.tsx` pour ouvrir un menu contextuel.
2.  Proposer de changer le shift (ex: passer de WORK 12h à REST, ou ajouter une absence).
3.  *Note technique :* L'enregistrement des modifications d'affectation n'est pas encore totalement couvert par une API de "mise à jour unitaire" sur le backend (à coordonner avec l'équipe backend si nécessaire).

---

## 4. Recommandations Techniques & Bonnes Pratiques

*   **Gestion des CORS :** Assurez-vous que le backend Django autorise les requêtes provenant du frontend Vite (généralement `localhost:5173`).
*   **State Management :** Si l'état devient trop complexe avec l'ajout de l'audit et des compteurs, envisagez d'introduire `React Query` (TanStack Query). Cela simplifiera grandement la gestion du cache, les re-fetch automatiques après la génération, et les états de chargement (`isLoading`).
*   **Tests :** Maintenez la couverture de tests. Mettez à jour les tests existants (`PlanningTable.test.tsx`, `usePlanning.test.ts`) pour vérifier les nouveaux comportements (Vérificateur, Couverture Souple).
