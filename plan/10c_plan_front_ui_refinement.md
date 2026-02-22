# PLAN FRONT 10c : Amélioration UX de la Grille de Planification

**Objectif :** Affiner l'interface utilisateur de la `PlanningTable` pour améliorer la lisibilité des plannings sur de longues périodes (ex: 12 semaines). Les axes d'amélioration sont : la navigation horizontale (colonne fixée), la densité de l'information (icônes) et la gestion temporelle internationale (dates en français avec une bibliothèque dédiée).

---

## 1. Analyse DDD et Stratégie (UI Refinement)

Nous restons dans le **Bounded Context** de la couche de **Présentation (UI State)**, plus particulièrement autour de la structuration des `Dumb Components`.

### Décisions Techniques et Design

1.  **Gestion des Dates (Time/Date Value Objects) :**
    - **Problème :** Manipuler des chaînes `YYYY-MM-DD` pour l'affichage est rigide et non localisé.
    - **Solution :** Utiliser la librairie `date-fns` (légère et modulaire) avec le locale `fr` (français) pour formatter les en-têtes de colonnes.
    - **Format UI :** Un en-tête sur deux niveaux. Ligne 1 : Date (ex: "01/02"), Ligne 2 : Jour abrégé (ex: "lun.").

2.  **Densité de l'Information (Cellules de la grille) :**
    - **Problème :** Le texte "WORK" ou "REST" prend trop de place en largeur, forçant un défilement fastidieux.
    - **Solution :** Remplacer le texte par des **icônes** standards (ex: `lucide-react` ou de simples emojis/SVG) :
      - 💼 (ou icône Briefcase) pour le travail.
      - 🏠 (ou icône Home/Coffee) pour le repos.
    - Conserver l'affichage des heures (ex: `12h`) en tout petit sous l'icône de travail pour ne pas perdre l'information de durée.

3.  **Ergonomie de Navigation (CSS / Layout) :**
    - **Problème :** Quand on scrolle vers la droite pour voir la fin du mois, on perd le nom de l'agent.
    - **Solution :** Utiliser CSS `position: sticky; left: 0;` sur la première colonne (Agent) ainsi qu'un `z-index` pour qu'elle survole le reste du tableau lors du défilement.

---

## 2. Plan de Développement (Séquence de Commits TDD)

Voici le plan pour le développeur React (`react-developer`).

1.  `build(deps): Install date-fns and lucide-react dependencies`
    *   *Objectif :* Ajouter les bibliothèques nécessaires à la manipulation des dates (`date-fns`) et aux icônes (`lucide-react`).
2.  `test(ui): Update PlanningTable tests for new date format and icons`
    *   *Objectif :* Modifier les tests existants de la `PlanningTable`. Remplacer la recherche des textes bruts (ex: "WORK", "2026-01-01") par la vérification du nouveau format français (ex: "01/01", "jeu.") et la présence d'éléments visuels.
3.  `feat(ui): Implement dual-row date headers in French`
    *   *Objectif :* Modifier le `<thead/>` de `PlanningTable.tsx` en utilisant `date-fns` (`format(date, 'dd/MM', { locale: fr })` et `format(date, 'E', { locale: fr })`).
4.  `feat(ui): Replace text shifts with Lucide icons`
    *   *Objectif :* Modifier les cellules de `PlanningTable.tsx` pour afficher les icônes (ex: `Briefcase` ou `Coffee`) à la place de "WORK" et "REST", afin de compresser la largeur des colonnes.
5.  `style(ui): Apply sticky positioning to the Agent column`
    *   *Objectif :* Ajouter les règles CSS en ligne ou dans `index.css` (ex: `position: sticky; left: 0; background: white;`) sur la première colonne (`<th>` et `<td>` "Agent") pour bloquer le défilement horizontal de cette colonne.
