# PLAN BACKEND 12 : API Endpoints pour Dashboard Configuration

**Objectif :** Exposer les données nécessaires au Frontend (Écran 1) pour configurer la génération de planning : liste des politiques, sélection multiple de politiques dans le solveur, et potentiellement mise à jour groupée des besoins quotidiens.

---

## 1. Analyse DDD (Backend)

Conformément au cahier des charges (Notion) :
- "Écran 1 : Dashboard Configuration (Input)"
- "Grille de saisie du besoin (7 colonnes)"
- "Liste des agents"

Le backend actuel possède des CRUD pour les agents et les besoins, mais il manque des choses pour fluidifier l'usage :

1.  **Compliance Engine (Moteur de Conformité) :**
    - Il n'y a pas d'API pour lister les politiques de conformité. Or le front en a besoin pour son formulaire.
2.  **Solver Engine (Générateur) :**
    - Actuellement, `/api/v1/solver/generate/` n'accepte qu'un seul `politique_id`. Le front doit pouvoir en envoyer plusieurs.
3.  **Demand Management (Besoins) :**
    - Le front va envoyer la "Grille de saisie du besoin" (7 jours). Il faut s'assurer que l'API permet de mettre à jour ces 7 jours facilement (peut-être un endpoint bulk update si les CRUD standards sont trop verbeux, mais pour l'instant on restera sur les CRUD standards si possible).

---

## 2. Plan de Développement (Séquence de Commits TDD)

Voici le plan pour le développeur Python (`ddd-developer`).

1.  `test(compliance): Add tests for PolitiqueConformite API endpoints`
    *   *Objectif :* Écrire les tests d'API vérifiant qu'un `GET /api/v1/compliance/politiques/` retourne bien la liste des politiques (nom, règles).
2.  `feat(compliance): Implement Serializer and ViewSet for Politiques`
    *   *Objectif :* Créer le serializer, le ViewSet et mettre à jour `urls.py` dans `compliance_engine` pour exposer les politiques en lecture seule (ou complète).
3.  `test(solver): Update solver API tests to handle multiple policies`
    *   *Objectif :* Modifier `test_acceptance_api.py` pour envoyer `politique_ids` (un tableau) au lieu de `politique_id` à l'endpoint POST `/api/v1/solver/generate/`.
4.  `feat(solver): Modify GenerateScheduleAPIView to accept politique_ids list`
    *   *Objectif :* Mettre à jour la validation du payload dans `GenerateScheduleAPIView` pour parser une liste d'UUIDs, récupérer les objets `PolitiqueConformiteModel` correspondants et gérer le cas de liste vide.
5.  `feat(solver): Update ScheduleSolverService to apply rules from multiple policies`
    *   *Objectif :* Modifier la signature de `solve` dans `ScheduleSolverService` pour accepter `politiques: List[PolitiqueConformite]` et injecter l'ensemble des règles de toutes ces politiques dans le modèle OR-Tools.
