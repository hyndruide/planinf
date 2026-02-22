# PLAN 07: Use Case "Gestion des Surnuméraires et Remplacement"

**Objectif :** Implémenter la logique d'absorption des absences. Lorsqu'un agent est absent, le système doit être capable d'identifier un agent en position de "Surnuméraire" sur la même trame pour le remplacer sans casser la logique du roulement global.

**Bounded Context :** `applied_planning` (évolution) & `resource_management` (évolution)

---

### Tâches de développement (pour le DEVELOPER) :

#### 1. Faire évoluer le domaine `Agent`
   - **Description :** Ajouter la notion de "Pool de remplacement" ou "Surnuméraire" au niveau contractuel de l'agent.
   - **Fichier :** `app/resource_management/domain/agent.py` & `models.py`
   - **Modifications :** Ajouter un attribut booléen `est_surnumeraire` (défaut: False).

#### 2. Modéliser les Absences (Exceptions de Trame)
   - **Description :** Créer une entité pour représenter une déviation par rapport à la trame théorique (ex: Congé Maladie, Congé Payé).
   - **Fichier :** `app/applied_planning/domain/absence.py` (nouveau) & `models.py`
   - **Agrégat :** `Absence(id, agent_id, date_debut, date_fin, type_absence)`
   - **Intégration :** Lier au modèle Django.

#### 3. Surcharger la Projection (PlanningService)
   - **Description :** Le `PlanningProjectionService` doit d'abord calculer la trame théorique, *puis* appliquer les absences par-dessus (remplacer `WORK` par `ABSENT`).
   - **Fichier :** `app/pattern_engine/domain/services.py` (ou dans `applied_planning/services.py` pour agglomérer).

#### 4. Service d'Identification des Remplaçants
   - **Description :** Créer un service applicatif qui, pour une absence donnée, cherche un agent `est_surnumeraire=True` qui devait être en `REST` ou `WORK_SURNUMERAIRE` ce jour-là sur la même trame.
   - **Fichier :** `app/applied_planning/services.py`
   - **Méthode :** `find_replacements_for_absence(absence: Absence) -> List[Agent]`
