# PLAN 05: Use Case "Projection de Planning"

**Objectif :** Implémenter la logique métier permettant de projeter le planning théorique d'un agent sur une période donnée. Cette fonctionnalité est le cœur du système : elle transforme la `Trame` (modèle statique) en une suite de jours travaillés/repos pour un `Agent` spécifique, en fonction de sa date de début de cycle.

**Bounded Context Principal :** `pattern_engine` (pour la logique de projection pure)
**Bounded Context Secondaire :** `applied_planning` (pour l'application à un agent)

---

### Tâches de développement (pour le DEVELOPER) :

#### 1. Setup de l'environnement de test
   - **Description :** Installer et configurer `pytest` et `factory_boy` pour faciliter l'écriture de tests robustes et lisibles.
   - **Fichier :** `pyproject.toml` (ajout des dépendances), `app/conftest.py` (configuration pytest).
   - **Commandes :** 
     - Ajouter `pytest`, `pytest-django`, `factory_boy` aux dépendances de développement via `poetry`.
     - Configurer `pytest.ini` pour pointer vers les settings Django.

#### 2. Implémenter la logique de projection dans `Trame`
   - **Description :** Ajouter une méthode métier à l'agrégat `Trame` capable de retourner le `Shift` correspondant à un index donné (jour du cycle).
   - **Fichier :** `app/pattern_engine/domain/trame.py`
   - **Méthode à ajouter :** `get_shift_at_day(day_index: int) -> Shift`
   - **Test :** `app/pattern_engine/tests/test_domain_trame.py` : Vérifier que la méthode retourne le bon shift et gère correctement le modulo (cycle infini).

#### 3. Créer le Service de Domaine `PlanningProjectionService`
   - **Description :** Ce service orchestre la projection. Il prend une `Trame`, une `date_debut_cycle` (pivot), et une période cible (`start_date`, `end_date`). Il retourne une liste de jours planifiés.
   - **Fichier :** `app/pattern_engine/domain/services.py`
   - **Classe :** `PlanningProjectionService`
   - **Méthode :** `project_planning(trame: Trame, date_debut_cycle: date, start_date: date, end_date: date) -> List[PlannedDay]`
   - **Note :** Il faudra définir une dataclass `PlannedDay(date: date, shift: Shift)` pour le retour.
   - **Test :** `app/pattern_engine/tests/test_domain_services.py` : Tester la projection sur plusieurs semaines, vérifier le bon calage par rapport à la date pivot.

#### 4. Intégrer le Use Case dans `applied_planning`
   - **Description :** Créer un point d'entrée applicatif (Service Applicatif) qui récupère l'affectation d'un agent et utilise le service de domaine pour générer son planning.
   - **Fichier :** `app/applied_planning/services.py`
   - **Méthode :** `get_agent_planning(agent_id: UUID, start_date: date, end_date: date)`
   - **Test d'intégration :** `app/applied_planning/tests/test_services.py` : Créer un agent, une trame, une affectation via les Factories, et vérifier que le planning sort correctement.
