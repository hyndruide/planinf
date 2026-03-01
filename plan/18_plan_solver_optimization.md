# PLAN 18 : Optimisation Finale du Solveur (OR-Tools)

**Objectif :** Rendre le `ScheduleSolverService` compatible avec les exigences réelles du terrain (décrites dans `fonctions.odt` et l'Excel), en introduisant les différents types de shifts (Matin, Soir, Nuit), la gestion des desiderata (Absences), et la tolérance aux erreurs (Soft Constraints) pour garantir la génération d'un planning même si le besoin ne peut pas être parfaitement couvert.

---

## 1. Analyse DDD & Modélisation Mathématique

### A. Différents Types de Shifts
Actuellement, la variable de décision est `work[(a, d)]` (Booléen : travaille ou ne travaille pas).
Il faut passer à un tenseur à 3 dimensions : **`shifts[(a, d, s)]`** où `s` est le type de shift (0=Repos, 1=Matin, 2=Soir, 3=Nuit).
*   *Contrainte forte :* Un agent ne peut faire qu'un seul type de shift par jour : `sum(shifts[(a, d, s)] for s in types) == 1`.

### B. Prise en compte des Desiderata (Absences préalables)
Le service doit accepter une liste d'absences pré-enregistrées.
*   *Injection OR-Tools :* Si l'agent `a` a posé un CA le jour `d`, on force la variable `shifts[(a, d, Repos)] == 1` avant même de lancer la résolution.

### C. Contraintes Souples (Soft Constraints) pour la Couverture
Au lieu d'imposer `sum(travaillent) >= besoin` (qui fait échouer le solveur si impossible), nous devons introduire des variables d'écart (slack variables).
*   Soit `present = sum(...)`
*   Variables entières : `under_staffed >= 0` et `over_staffed >= 0`
*   Équation : `present + under_staffed - over_staffed == besoin`
*   **Fonction d'objectif :** On minimise massivement ces variables d'écart (`Minimize(under_staffed * 1000 + over_staffed * 500 + équité)`).

---

## 2. Tâches de développement (pour le DEVELOPER) :

### Étape 1 : Préparation du Domaine
1.  **Mettre à jour `DailyRequirement`** : Il doit spécifier le besoin *par type de shift*. (ex: 2 le Matin, 1 le Soir). Si ce n'est pas possible de changer la BD tout de suite, on peut simuler un besoin global qui peut être couvert par n'importe quel shift pour ce plan.
2.  **Mettre à jour la signature de `solve`** : 
    `def solve(self, agents, requirements, politiques, duree_cycle_jours, absences: List[Absence] = [])`

### Étape 2 : Réécriture du Modèle CP-SAT (`ScheduleSolverService`)
1.  **Variables 3D** : Remplacer `work[(a, d)]` par `shifts[(a, d, shift_type)]`.
    *   Exemple de types : `0: REST`, `1: WORK_DAY_12H`. (Pour une transition douce, on garde un seul type de travail pour l'instant, mais on prépare la matrice pour pouvoir ajouter MATIN/SOIR plus tard).
2.  **Injection des Absences** : Boucler sur la liste des absences fournies. Convertir la date de l'absence en index `d` (jour du cycle). Ajouter la contrainte : `model.Add(shifts[(a, d, REST)] == 1)`.
3.  **Contraintes Souples (Soft Constraints)** :
    *   Retirer la contrainte de couverture stricte.
    *   Créer `under_staff[(d)]` et `over_staff[(d)]`.
    *   Ajouter `model.Add(sum(...) + under_staff[(d)] - over_staff[(d)] == besoin)`.
4.  **Nouvel Objectif** :
    *   Garder la logique d'équité (différence min/max des jours travaillés).
    *   Ajouter des poids lourds pour les écarts d'effectifs :
    *   `model.Minimize(sum(under_staff)*1000 + sum(over_staff)*500 + difference_equite)`

### Étape 3 : Tests (TDD)
1.  **Mettre à jour / Créer un test `test_solver_with_absences_and_soft_constraints`** :
    *   Créer 3 agents. Demander un besoin de 4 (impossible à couvrir).
    *   Poser une absence pour l'agent 1 le jour 0.
    *   Vérifier que `solve()` ne retourne pas `None`, mais retourne bien un planning.
    *   Vérifier que l'agent 1 est bien en `REST` le jour 0.
    *   Vérifier que le planning signale un manque d'effectif via le coverage (le besoin n'est pas atteint mais le planning existe).
