# USM - Unit Schedule Manager

USM est une application de gestion de plannings hospitaliers conçue avec une architecture **Domain-Driven Design (DDD)**. Elle permet d'automatiser la génération de roulements complexes (12h, 2x8, 3x8) tout en garantissant la conformité avec le code du travail.

## 🚀 Architecture du Projet

Le projet est structuré en **Monorepo** :
- `/app` : Backend Django (Python 3.12+, Poetry).
- `/frontend` : Frontend React (Vite, TypeScript, Tailwind CSS).
- `/skills` : Agents spécialisés (Planner, Developer, Reviewer) pour l'assistance au développement.

---

## 🛠️ Guide de démarrage (Backend)

### 1. Installation
Assurez-vous d'avoir `poetry` installé.
```bash
poetry install
```

### 2. Lancement du serveur
```bash
poetry run python app/manage.py runserver
```
L'interface d'administration est accessible sur `http://127.0.0.1:8000/admin/`.

---

## 📖 Comment utiliser le moteur de planning ?

Le système repose sur la transformation d'une **Trame Théorique** en un **Planning Réel**.

### Étape 1 : Créer une Trame (Pattern)
Une `Trame` est une séquence de `Shifts` (travail ou repos) qui se répète de manière cyclique (ex: 14 jours, 84 jours).
- Allez dans `api/v1/patterns/trames/` (POST) ou via l'Admin.
- Définissez la `sequence_data`. Exemple pour un cycle 2-2 :
  `[{"type": "WORK", "duration": 12}, {"type": "WORK", "duration": 12}, {"type": "REST", "duration": 0}, {"type": "REST", "duration": 0}]`

### Étape 2 : Créer un Agent
Un `Agent` possède une `date_debut_cycle`. C'est le point de départ "J0" de son roulement.
- Allez dans `api/v1/resources/agents/`.

### Étape 3 : Créer une Affectation
L' `Affectation` lie un Agent à une Trame à une date précise. 
- **Validation Active :** Lors de la création, le **Moteur de Conformité** projette le planning sur 12 semaines. Si l'affectation provoque une violation (ex: moins de 11h de repos entre deux shifts), la sauvegarde est rejetée.

### Étape 4 : Visualiser le Planning et la Couverture
Le moteur calcule dynamiquement la projection :
- **Planning Global :** `GET /api/v1/planning/full-view/?start_date=2026-02-16`
- **Analyse de Santé :** `GET /api/v1/coverage/analysis/?start_date=2026-02-16&end_date=2026-02-22`
  *(Compare les agents présents vs le `DailyRequirement` défini par le manager).*

---

## 🛡️ Règles de Conformité
Le moteur intègre les règles suivantes :
- **RegleReposMinQuotidien** : Vérifie les 11h de repos obligatoires.
- **RegleHeuresMaxHebdo** : Vérifie le plafond de 48h/semaine.
- **RegleReposDominical** : Vérifie la fréquence des dimanches de repos.

---

## 🧪 Tests
Le projet suit une approche TDD rigoureuse.
```bash
poetry run pytest
```
Un test d'acceptance complet est disponible dans `app/applied_planning/tests/test_acceptance.py`.
