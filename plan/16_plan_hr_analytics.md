# PLAN 16 : Analytique RH et Calcul des ETP (Heures de Nuit / Dimanches)

**Objectif :** Fournir les rapports globaux demandés par la DRH, en reproduisant la logique des feuilles `Annexe - Calcul des ETP` et la séparation des bases horaires (Nuit vs Jour) du fichier Excel.

**Contexte issu de l'analyse du fichier Excel :**
L'Excel distingue la `base horaire 35h / 37h30` de la `base horaire de nuit`. Les agents de nuit ont souvent des règles et des calculs d'heures différents. L'Excel sert aussi à agréger les données de tous les agents pour sortir un nombre total d'Equivalent Temps Plein (ETP) déployés sur le terrain.

---

## 1. Extension du Bounded Context : `resource_management` et `applied_planning`

### 2. Tâches de développement (pour le DEVELOPER) :

1.  **Gestion des Heures Spécifiques (Nuit / Dimanche)**
    *   Mettre à jour le domaine `pattern_engine.domain.shift` pour pouvoir tagger un shift (ex: `is_night_shift=True` ou une plage horaire explicite `start_time=20:00, end_time=08:00`).
2.  **Service de Rapport ETP (FTE Reporting)**
    *   Créer un service qui consolide l'ensemble des plannings d'un service sur un mois donné.
    *   Calculer l'ETP réel = (Total des heures planifiées pour tous les agents) / (Base légale mensuelle 151.67h).
3.  **API REST**
    *   Exposer un endpoint `GET /api/v1/planning/reports/fte/?month=...` retournant l'ETP cible (somme des quotités des contrats) vs l'ETP réel planifié.
4.  **Tests (TDD)**
    *   Créer 3 agents à 100% (Quotité 1.0) et 1 agent à 50% (Quotité 0.5). L'ETP cible est de 3.5.
    *   Générer un planning pour le mois.
    *   Le rapport doit calculer correctement la somme des heures et la division pour trouver l'ETP réel.
