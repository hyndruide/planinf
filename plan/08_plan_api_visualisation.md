# PLAN 08: Use Case "API REST pour la Visualisation (Frontend React)"

**Objectif :** Exposer les données calculées (Trames, Projections, Couverture) via une API REST (Django REST Framework) pour permettre au Frontend React de construire le tableau de bord (Matrice de 12 semaines, Indicateur de santé).

**Bounded Context :** Tous (Couche Interface/API)

---

### Tâches de développement (pour le DEVELOPER) :

#### 1. Setup Django REST Framework (DRF)
   - **Description :** Installer et configurer DRF dans le projet.
   - **Fichier :** `pyproject.toml` (ajout de `djangorestframework`), `app/planinf/settings.py` (INSTALLED_APPS), `app/planinf/urls.py`.

#### 2. Endpoint : Récupération du Planning Global (Matrice)
   - **Description :** Créer une vue API qui renvoie la liste des agents avec leurs shifts projetés sur une période donnée (ex: 3 mois). C'est ce qui alimentera l'Écran 2 (Visualiseur de Trame).
   - **Fichier :** `app/applied_planning/api/views.py` & `serializers.py`
   - **URL :** `GET /api/v1/planning/full-view/?start_date=YYYY-MM-DD&weeks=12`
   - **Format de sortie :** Adapté au Frontend (ex: liste d'agents, chacun contenant une liste de shifts quotidiens).

#### 3. Endpoint : Analyse de Couverture (Santé)
   - **Description :** Créer une vue API qui renvoie le rapport de couverture (besoin vs présents) pour alimenter la jauge de santé du planning.
   - **Fichier :** `app/demand_management/api/views.py` & `serializers.py`
   - **URL :** `GET /api/v1/coverage/analysis/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

#### 4. Tests d'API
   - **Description :** Écrire des tests pour s'assurer que les endpoints retournent les bons codes HTTP (200) et le bon format JSON, en s'appuyant sur les services métiers déjà testés.
