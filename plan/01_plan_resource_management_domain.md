# PLAN 01: Domaine du Bounded Context "Gestion des Ressources"

**Objectif :** Définir les modèles de base (domaine) pour représenter les employés et leurs attributs contractuels. C'est le socle sur lequel reposera toute la logique de planification.

**Bounded Context :** `resource_management`

---

### Tâches de développement (pour le DEVELOPER) :

#### 1. Créer le Value Object `Quotite`
   - **Description :** Représente le temps de travail contractuel d'un agent. C'est un objet de valeur car il n'a pas d'identité propre (80% est toujours 80%).
   - **Fichier :** `app/resource_management/domain/quotite.py`
   - **Attributs :**
     - `value` (float) : ex: 1.0, 0.8, 0.5
   - **Règles métier :**
     - La valeur doit être comprise entre 0 et 1.
     - Doit être immutable.

#### 2. Créer l'Aggregate `Agent`
   - **Description :** C'est l'Aggregate Root. Il représente un employé du service.
   - **Fichier :** `app/resource_management/domain/agent.py`
   - **Attributs :**
     - `id` (UUID) : Identifiant unique.
     - `nom` (str) : Nom de l'agent.
     - `quotite` (Quotite) : Le Value Object défini ci-dessus.
     - `date_debut_cycle` (date) : La date de départ sur laquelle se base le calcul de sa position dans une trame.

#### 3. Mettre en place la structure des répertoires
   - Créer les répertoires `app/resource_management/` et `app/resource_management/domain/`.
   - Ajouter les fichiers `__init__.py` nécessaires pour que Python reconnaisse les modules.
