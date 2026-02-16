# PLAN 02: Domaine du Bounded Context "Moteur de Trames"

**Objectif :** Modéliser la structure d'un roulement théorique. C'est le "patron" réutilisable qui décrit une séquence de travail avant qu'elle ne soit appliquée à des agents réels.

**Bounded Context :** `pattern_engine`

---

### Tâches de développement (pour le DEVELOPER) :

#### 1. Créer le Value Object `Shift`
   - **Description :** Représente une vacation de travail ou un repos. Il est défini par son type et sa durée.
   - **Fichier :** `app/pattern_engine/domain/shift.py`
   - **Attributs :**
     - `type` (Enum) : `WORK`, `REST`.
     - `duration` (int) : Durée en heures (ex: 12, 0).
   - **Règles métier :**
     - La durée ne peut pas être négative.
     - Si `type` est `REST`, la durée doit être 0.
     - Doit être immutable.

#### 2. Créer l'Aggregate `Trame` (Pattern)
   - **Description :** C'est l'Aggregate Root de ce contexte. Il représente une Trame Maître, un modèle de roulement complet sur une période donnée (ex: 14 jours, 84 jours).
   - **Fichier :** `app/pattern_engine/domain/trame.py`
   - **Attributs :**
     - `id` (UUID) : Identifiant unique de la trame.
     - `nom` (str) : Nom descriptif (ex: "Roulement 12h - Petite/Grande Semaine").
     - `duree_cycle_jours` (int) : Durée totale du cycle en jours (ex: 14).
     - `sequence` (List[Shift]) : La liste ordonnée des `Shift` qui composent la trame.
   - **Règles métier :**
     - La longueur de la `sequence` doit être égale à `duree_cycle_jours`.
     - Le nom de la trame ne peut pas être vide.

#### 3. Mettre en place la structure des répertoires
   - Créer les répertoires `app/pattern_engine/` et `app/pattern_engine/domain/`.
   - Ajouter les fichiers `__init__.py` nécessaires.
