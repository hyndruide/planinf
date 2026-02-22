# PLAN 11: Moteur de Génération Automatique de Trame (Solver OR-Tools)

**Objectif :** Implémenter un algorithme de résolution sous contraintes (Solver) capable de générer automatiquement une `Trame` optimale et les `Affectation` correspondantes pour un groupe d'agents, en fonction des besoins (Effectif Cible) et des règles légales (Code du travail).

**Nouveau Bounded Context :** `solver_engine` (Moteur de résolution)

---

### Tâches de développement (pour le DEVELOPER) :

#### 1. Installation de Google OR-Tools
   - **Description :** Ajouter la librairie OR-Tools au projet.
   - **Commandes :** `poetry add ortools`

#### 2. Création du domaine `solver_engine`
   - **Description :** Créer un service de domaine qui encapsule la complexité mathématique d'OR-Tools.
   - **Fichier :** `app/solver_engine/domain/solver_service.py`
   - **Classe :** `ScheduleSolverService`
   - **Méthode principale :** `solve(agents: List[Agent], requirements: List[DailyRequirement], politique: PolitiqueConformite, duree_cycle_jours: int) -> Optional[Dict[UUID, Trame]]`
   - **Logique interne (OR-Tools CP-SAT) :**
     - Créer le modèle CP-SAT (`cp_model.CpModel()`).
     - **Variables :** Créer une matrice booléenne `shifts[(agent_id, jour, type_shift)]` (1 si l'agent fait ce shift ce jour-là, 0 sinon).
     - **Contraintes de couverture (Besoins) :** Pour chaque jour, la somme des agents en `WORK` doit être `>=` au `required_count` de ce jour de la semaine.
     - **Contraintes légales (Compliance) :** Traduire les règles de `PolitiqueConformite` en contraintes mathématiques OR-Tools (ex: pas plus de X heures de travail d'affilée, 11h de repos minimum entre deux shifts de travail, etc.).
     - **Contrainte d'unicité :** Un agent ne peut faire qu'un seul type de shift par jour (WORK ou REST).
     - **Objectif (Optimisation) :** Minimiser le surplus d'agents ou maximiser l'équité des week-ends (selon la complexité voulue, on peut commencer par juste chercher "une solution satisfaisante" sans fonction d'objectif complexe).
     - **Solveur :** Lancer la résolution (`cp_model.CpSolver()`).
     - **Extraction :** Si une solution est trouvée (`OPTIMAL` ou `FEASIBLE`), transformer la matrice résultante en objets `Trame` (ou une Trame Maître commune avec des décalages/offsets pour chaque agent) et retourner le résultat.

#### 3. Service Applicatif d'Orchestration
   - **Description :** Créer un service qui prépare les données pour le solver, le lance, et persiste les résultats (création des objets `TrameModel` et `AffectationModel` en base).
   - **Fichier :** `app/solver_engine/services.py`
   - **Méthode :** `generate_and_save_schedule(agent_ids: List[UUID], politique_id: UUID, duree_cycle: int, date_debut: date)`

#### 4. API REST pour le Générateur
   - **Description :** Exposer un endpoint POST pour déclencher la génération automatique depuis le frontend.
   - **Fichier :** `app/solver_engine/api/views.py` & `urls.py`
   - **URL :** `POST /api/v1/solver/generate/`
   - **Payload :** `{ "agent_ids": [...], "politique_id": "...", "duree_cycle": 84, "date_debut": "YYYY-MM-DD" }`

#### 5. Tests
   - **Description :** Écrire un test unitaire robuste pour le `ScheduleSolverService` vérifiant qu'il trouve bien une solution pour un cas simple (ex: 4 agents, besoin de 2/jour, cycle 14 jours, règle 11h repos) et qu'il renvoie `None` si le problème est impossible (ex: besoin de 5 agents mais seulement 3 agents disponibles).
