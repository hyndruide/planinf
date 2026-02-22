# PLAN 09: Use Case "Validation Active par le Moteur de Conformité"

**Objectif :** Connecter le moteur de conformité (créé au Plan 04) au processus de création/modification des trames et des affectations. Le système doit rejeter toute planification qui enfreint les règles légales (ex: > 48h/semaine).

**Bounded Context :** `compliance_engine` (intégration avec le reste)

---

### Tâches de développement (pour le DEVELOPER) :

#### 1. Implémenter l'évaluation des Règles
   - **Description :** Ajouter la logique d'évaluation au sein du `compliance_engine`. Chaque objet `Regle` (ex: `RegleHeuresMaxHebdo`) doit avoir une méthode `is_satisfied_by(planning: List[PlannedDay]) -> bool`.
   - **Fichier :** `app/compliance_engine/domain/evaluators.py` (ou dans `regles.py`).
   - **Test unitaire :** Vérifier que la règle des 48h échoue si on simule 5 shifts de 12h dans la même semaine.

#### 2. Service de Validation de Politique
   - **Description :** Créer un service de domaine qui prend un planning projeté et une `PolitiqueConformite`, et évalue toutes les règles de la politique.
   - **Fichier :** `app/compliance_engine/domain/services.py`
   - **Méthode :** `validate_planning(planning: List[PlannedDay], politique: PolitiqueConformite) -> ResultatValidation`

#### 3. Intégration dans la Création de Trame/Affectation (API ou Admin)
   - **Description :** Faire en sorte que lors de la sauvegarde d'une nouvelle `Affectation` (ou via un endpoint API `POST /api/v1/planning/validate/`), le système génère une projection "virtuelle" sur 12 semaines et la passe au moteur de conformité.
   - **Comportement :** Si la validation échoue (règle bloquante), l'opération est annulée et une erreur métier claire est renvoyée à l'utilisateur.
