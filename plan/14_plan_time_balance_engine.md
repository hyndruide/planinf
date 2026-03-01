# PLAN 14 : Moteur de Balance Horaire (Time Balance Engine)

**Objectif :** Remplacer les calculs complexes des feuilles Excel `CalculsX` (qui calculent les dépassements d'heures) par un moteur Backend robuste capable de suivre la balance horaire de chaque agent sur un cycle donné.

**Contexte issu de l'analyse du fichier Excel :**
Le fichier `Planning Cycles AS.xlsm` utilise les feuilles `Calculs12` à `Calculs2` pour cumuler les heures travaillées jour par jour. Il compare ces heures à une base horaire (ex: 35h ou 37h30), applique la quotité de l'agent (ex: 80%), et calcule un "dépassement" (Crédit ou Débit d'heures) à la fin de chaque semaine et à la fin du cycle. Il gère également l'acquisition des RTT.

---

## 1. Nouveau Bounded Context ou Module : `time_tracking` (ou extension de `applied_planning`)

Nous allons créer un service dédié au calcul des balances horaires.

### Modèles du Domaine (Domain Models)
- **`ContratBase`** : Définit la base horaire (35h, 37.5h) et le droit aux RTT.
- **`TimeBalanceReport`** : Objet de valeur (Value Object) contenant le résultat du calcul pour un agent sur un cycle (heures travaillées, heures dues, balance finale).
- **`WeeklyBalance`** : Détail du calcul par semaine.

### 2. Tâches de développement (pour le DEVELOPER) :

1.  **Création du Domaine `time_tracking`**
    *   Créer `app/time_tracking/domain/balance.py`.
    *   Implémenter la logique de calcul : `(Heures Travaillées) - (Base Hebdo * Quotité) = Balance Hebdo`.
    *   Gérer les RTT : Si la base est de 37h30, l'agent acquiert des RTT.
2.  **Service Applicatif (`TimeBalanceService`)**
    *   Créer une méthode `calculate_cycle_balance(agent_id, start_date, end_date)` qui récupère les `Affectation` et les `Shift` (via `applied_planning` et `pattern_engine`) et retourne un `TimeBalanceReport`.
3.  **API REST**
    *   Exposer un endpoint `GET /api/v1/planning/agents/{id}/balance/?start_date=...&end_date=...` pour que le Frontend puisse afficher les compteurs d'heures.
4.  **Tests (TDD)**
    *   Simuler un cycle de 14 jours avec un agent à 100% sur 35h, travaillant 7 shifts de 12h (soit 84h).
    *   Le besoin normal pour 2 semaines est de 70h (35h * 2).
    *   La balance finale doit afficher un excédent (dépassement) de +14h.
