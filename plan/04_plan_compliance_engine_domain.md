# PLAN 04 (Révisé): Domaine du Bounded Context "Moteur de Conformité"

**Objectif :** Modéliser un ensemble de règles de conformité (une "politique") sous une forme directement utilisable par un algorithme de génération de planning. Ces objets définiront les contraintes à respecter *pendant* la création des trames.

**Bounded Context :** `compliance_engine`

---

### Tâches de développement (pour le DEVELOPER) :

#### 1. Créer une hiérarchie de Value Objects pour les Règles
   - **Description :** Créer des classes spécifiques et typées pour chaque type de règle afin qu'elles soient compréhensibles par le système. Toutes ces classes seront des objets de valeur immutables.
   - **Fichier :** `app/compliance_engine/domain/regles.py`
   - **Classes à définir :**
     - `RegleHeuresMaxJournalieres(max_heures: int)`
     - `RegleReposMinQuotidien(min_heures_repos: int)`
     - `RegleHeuresMaxHebdo(max_heures: int)`
     - `RegleMoyenneHeuresHebdo(moyenne_heures: int, periode_lissage_semaines: int)`
     - `RegleReposDominical(frequence: int)` (ex: 1 dimanche sur `frequence`=2)

#### 2. Créer l'Aggregate `PolitiqueConformite`
   - **Description :** C'est l'Aggregate Root. Il représente un ensemble cohérent de règles (par exemple, "Convention FPH", "CCN 51"). Le moteur de génération de planning prendra une de ces politiques en entrée.
   - **Fichier :** `app/compliance_engine/domain/politique.py`
   - **Attributs :**
     - `id` (UUID) : Identifiant unique de la politique.
     - `nom` (str) : Nom de la politique (ex: "Politique Standard Hôpital Public").
     - `regles` (List[Union[...]]) : Une liste contenant des instances des différentes classes de règles définies ci-dessus.

#### 3. Mettre à jour la structure des répertoires
   - Créer les répertoires `app/compliance_engine/` et `app/compliance_engine/domain/`.
   - Créer les fichiers `regles.py`, `politique.py` et les `__init__.py` nécessaires.
