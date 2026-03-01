# PLAN 13 : Intégration Dynamique de la Conformité dans le Solveur OR-Tools

**Objectif :** Modifier le moteur de résolution (`ScheduleSolverService`) pour qu'il n'utilise plus de contraintes codées en dur (ex: max 3 jours consécutifs), mais qu'il traduise dynamiquement les règles issues des politiques de conformité (`PolitiqueConformite`) en contraintes mathématiques pour OR-Tools.

---

## 1. Analyse DDD (Backend)

Actuellement, le `ScheduleSolverService` crée un modèle CP-SAT mais ignore les règles (`RegleHeuresMaxJournalieres`, `RegleReposMinQuotidien`, `RegleHeuresMaxHebdo`, `RegleMoyenneHeuresHebdo`, `RegleReposDominical`) passées via l'objet `PolitiqueConformite` (ou la liste de politiques). À la place, il applique une contrainte statique pour forcer un roulement.

Pour que le solveur produise un planning légalement valide, il faut parser chaque règle de la (ou les) politique(s) et appliquer la contrainte correspondante sur les variables de décision (`work[(a, d)]`).

*Note : Pour le moment, le solveur suppose que chaque jour travaillé correspond à un shift de 12 heures (cf. `Shift(ShiftType.WORK, 12)`). Les contraintes basées sur les heures devront utiliser cette hypothèse (1 jour de travail = 12h).*

---

## 2. Traduction des Règles en Contraintes OR-Tools

Le développeur devra implémenter une logique (par exemple via un pattern Visiteur ou un dictionnaire de mapping par type de règle) pour ajouter les contraintes au `model` :

1.  **`RegleHeuresMaxHebdo`**
    *   *Principe :* La somme des heures sur 7 jours glissants ne doit pas dépasser le max.
    *   *Implémentation :* Pour chaque agent `a` et chaque jour de début de semaine glissante `d`, `sum(work[(a, d+i)] * 12 for i in range(7)) <= max_heures`.

2.  **`RegleMoyenneHeuresHebdo`**
    *   *Principe :* La moyenne des heures sur le cycle ne doit pas dépasser un seuil.
    *   *Implémentation :* `sum(work[(a, d)] * 12 for d in range(num_days)) <= (moyenne_heures * num_days) / 7`.

3.  **`RegleReposDominical`**
    *   *Principe :* Au moins 1 dimanche sur N doit être non travaillé (REST).
    *   *Implémentation :* Identifier les indices `d` correspondant à des dimanches. Pour chaque agent `a` et chaque fenêtre de N dimanches, `sum(work[(a, dimanche_index)]) <= N - 1`.

4.  **`RegleReposMinQuotidien` / `RegleHeuresMaxJournalieres`**
    *   *Principe :* Si on reste sur des shifts fixes de 12h, certaines de ces règles sont satisfaites par défaut, ou peuvent être converties en "Pas plus de X jours consécutifs". Une réflexion sera nécessaire pour les adapter au modèle mathématique.

---

## 3. Plan de Développement (Séquence de Commits TDD)

Voici le plan pour le développeur Python (`ddd-developer`).

1.  `test(solver): Add failing tests for dynamic policy rules in solver`
    *   *Objectif :* Mettre à jour `test_domain_solver.py` pour tester spécifiquement que le solveur échoue (ou modifie son comportement) quand on lui passe une `RegleHeuresMaxHebdo(36)` (qui empêcherait de travailler plus de 3 jours de 12h par semaine glissante) ou une `RegleReposDominical(2)`.
    *   *Vérification :* Le test doit échouer car le solveur actuel a sa propre règle en dur.

2.  `feat(solver): Remove hardcoded constraints and setup dynamic rule parser`
    *   *Objectif :* Supprimer la contrainte en dur (`work + work+1 + work+2 + work+3 <= 3`) dans `ScheduleSolverService.solve()`. Créer la structure (ex: boucle `for regle in politique.regles:`) pour appliquer les contraintes.

3.  `feat(solver): Implement RegleHeuresMaxHebdo constraint in OR-Tools`
    *   *Objectif :* Ajouter la logique pour traduire `RegleHeuresMaxHebdo` en équations OR-Tools (fenêtre glissante de 7 jours).

4.  `feat(solver): Implement RegleReposDominical constraint in OR-Tools`
    *   *Objectif :* Ajouter la logique pour traduire `RegleReposDominical` en équations OR-Tools. (Gérer le modulo 7 pour identifier les dimanches par rapport au `duree_cycle_jours`).

5.  `feat(solver): Implement RegleMoyenneHeuresHebdo constraint in OR-Tools`
    *   *Objectif :* Ajouter la logique pour traduire `RegleMoyenneHeuresHebdo` sur la durée totale du cycle.

6.  `refactor(solver): Handle multiple policies in ScheduleSolverService`
    *   *Objectif :* S'assurer que le solveur boucle bien sur *toutes* les politiques (si on passe une liste, comme prévu dans le plan 12) et accumule l'ensemble des règles sans conflits.
    *   *Vérification :* Tous les tests du domaine et les tests d'acceptance passent.
