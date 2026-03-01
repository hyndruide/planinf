# PLAN 15 : Service d'Audit et de Vérification (Le "Vérificateur")

**Objectif :** Remplacer l'onglet `Vérificateur` et les feuilles `RHX` du fichier Excel. Fournir une API capable d'auditer n'importe quel planning (généré ou modifié manuellement) et de remonter précisément les jours non conformes (`NC`).

**Contexte issu de l'analyse du fichier Excel :**
Dans Excel, les feuilles `RH12` à `RH2` utilisent des formules conditionnelles massives (ex: `=IF(L34="NC","NC",IF(OR(L34="",L34="ok",L34>=$I$3),"ok","NC"))`) pour vérifier chaque jour si le repos quotidien (11h) ou le repos hebdomadaire (35h) est respecté.

Notre `compliance_engine` sait déjà bloquer le solveur si une règle n'est pas respectée, mais il ne sait pas "auditer" un planning existant pour dire *exactement quel jour* pose problème à l'utilisateur.

---

## 1. Extension du Bounded Context : `compliance_engine`

### Nouveaux Modèles du Domaine (Domain Models)
- **`AuditResult`** : Résultat global (Conforme / Non Conforme).
- **`DailyComplianceStatus`** : Détail pour un jour donné (Date, Règle évaluée, Statut "OK" ou "NC", Message d'erreur).

### 2. Tâches de développement (pour le DEVELOPER) :

1.  **Modification du `compliance_engine.domain.regles`**
    *   Ajouter une méthode `audit(planning: List[PlannedDay]) -> List[DailyComplianceStatus]` à chaque classe de règle (`RegleReposMinQuotidien`, `RegleHeuresMaxHebdo`, etc.).
    *   Au lieu de retourner juste `True` ou `False`, cette méthode doit retourner une liste identifiant les jours précis où la règle a été enfreinte.
2.  **Service Applicatif d'Audit**
    *   Créer `AuditService.run_audit(agent_id, start_date, end_date)`.
    *   Ce service charge le planning de l'agent, charge les politiques de conformité qui lui sont applicables, et exécute les règles d'audit.
3.  **API REST**
    *   Exposer un endpoint `GET /api/v1/compliance/audit/?agent_id=...&start_date=...&end_date=...`
    *   Le frontend l'utilisera pour afficher des alertes rouges sur les jours problématiques dans le tableau du planning.
4.  **Tests (TDD)**
    *   Créer un planning factice (Mock) où un agent travaille deux shifts de 12h séparés de seulement 8h de repos.
    *   Appeler le service d'audit avec une `RegleReposMinQuotidien(11)`.
    *   Vérifier que le service retourne "NC" spécifiquement pour la date du deuxième shift.
