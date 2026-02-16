# PLAN 03: Domaine du Bounded Context "Planification Appliquée"

**Objectif :** Définir comment un agent est affecté à une trame théorique. Ce contexte fait le lien entre une ressource (`Agent`) et un modèle de travail (`Trame`).

**Bounded Context :** `applied_planning`
**Dépendances Inter-Contextes :**
- `resource_management.Agent` (via son ID)
- `pattern_engine.Trame` (via son ID)

---

### Tâches de développement (pour le DEVELOPER) :

#### 1. Créer l'Aggregate `Affectation`
   - **Description :** C'est l'Aggregate Root de ce contexte. Il représente le lien pivot entre un agent et une trame, formant ainsi la base d'un planning réel.
   - **Fichier :** `app/applied_planning/domain/affectation.py`
   - **Attributs :**
     - `id` (UUID) : Identifiant unique de l'affectation.
     - `agent_id` (UUID) : L'identifiant de l'`Agent` (du contexte `resource_management`).
     - `trame_id` (UUID) : L'identifiant de la `Trame` (du contexte `pattern_engine`).
     - `date_debut` (date) : La date à laquelle l'agent commence cette affectation de trame.

   - **Règles métier :**
     - Une `Affectation` doit toujours être liée à un `agent_id` et une `trame_id` valides.

#### 2. Mettre en place la structure des répertoires
   - Créer les répertoires `app/applied_planning/` et `app/applied_planning/domain/`.
   - Ajouter les fichiers `__init__.py` nécessaires.
