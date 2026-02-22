import pytest
from datetime import date
from django.core.exceptions import ValidationError

from resource_management.models import AgentModel
from pattern_engine.models import TrameModel
from pattern_engine.domain.shift import Shift, ShiftType
from compliance_engine.models import PolitiqueConformiteModel
from applied_planning.models import AffectationModel
from demand_management.models import DailyRequirementModel
from demand_management.services import get_coverage_analysis

@pytest.mark.django_db
def test_acceptance_planning_84_jours_avec_regle_11h():
    """
    Test d'acceptance :
    - Création d'une politique de conformité exigeant 11h de repos minimum par jour (donc max 13h de travail).
    - Création de besoins (Effectif cible de 2 agents par jour).
    - Création d'une trame valide sur 84 jours (cycles de 12h, 2 jours on, 2 jours off).
    - Affectation d'agents avec différents décalages pour couvrir le besoin.
    - Vérification que la couverture est bien atteinte (0 gap).
    - Tentative d'affectation sur une trame avec des shifts de 14h, qui doit être rejetée par le moteur de conformité.
    """
    
    # 1. Définition de la politique légale (11h de repos min)
    politique = PolitiqueConformiteModel.objects.create(
        nom="Code du travail - 11h repos",
        regles_data=[
            {
                "__type__": "RegleReposMinQuotidien",
                "min_heures_repos": 11
            }
        ]
    )

    # 2. Définition du besoin (2 agents requis chaque jour de la semaine)
    for day_idx in range(7):
        DailyRequirementModel.objects.create(day_of_week=day_idx, required_count=2)

    # 3. Création d'une Trame Maître de 84 jours valide
    # Pattern: 2 jours de travail (12h), 2 jours de repos
    sequence_valide = []
    for _ in range(21): # 21 * 4 jours = 84 jours
        sequence_valide.extend([
            Shift(ShiftType.WORK, 12),
            Shift(ShiftType.WORK, 12),
            Shift(ShiftType.REST, 0),
            Shift(ShiftType.REST, 0),
        ])
    
    trame_valide = TrameModel.objects.create(
        nom="Roulement 12h 2-2",
        duree_cycle_jours=84,
        sequence_data=sequence_valide
    )

    # 4. Création des agents et affectations pour couvrir le besoin
    # On affecte 2 agents au début du cycle (ils travailleront J0 et J1)
    date_depart = date(2026, 1, 1)
    
    agent_a = AgentModel.objects.create(nom="Alice", date_debut_cycle=date_depart)
    agent_b = AgentModel.objects.create(nom="Bob", date_debut_cycle=date_depart)
    
    AffectationModel.objects.create(agent=agent_a, trame=trame_valide, date_debut=date_depart)
    AffectationModel.objects.create(agent=agent_b, trame=trame_valide, date_debut=date_depart)

    # Pour couvrir J2 et J3 (quand Alice et Bob sont en repos), 
    # on crée 2 autres agents décalés de 2 jours en arrière
    date_decalee = date(2025, 12, 30)
    
    agent_c = AgentModel.objects.create(nom="Charlie", date_debut_cycle=date_decalee)
    agent_d = AgentModel.objects.create(nom="Diana", date_debut_cycle=date_decalee)
    
    AffectationModel.objects.create(agent=agent_c, trame=trame_valide, date_debut=date_decalee)
    AffectationModel.objects.create(agent=agent_d, trame=trame_valide, date_debut=date_decalee)

    # 5. Vérification de la couverture générée
    # On analyse la couverture sur les 4 premiers jours de 2026
    report = get_coverage_analysis(date(2026, 1, 1), date(2026, 1, 4))
    
    assert len(report) == 4
    for jour_analyse in report:
        assert jour_analyse.required_count == 2
        assert jour_analyse.present_count == 2
        assert jour_analyse.gap == 0, f"Déficit/Surplus détecté le {jour_analyse.date}"

    # 6. Vérification du Moteur de Conformité (Rejet d'une trame illégale)
    # On crée une trame avec des shifts de 14h (laisse seulement 10h de repos)
    sequence_invalide = [Shift(ShiftType.WORK, 14)] * 84
    trame_invalide = TrameModel.objects.create(
        nom="Trame Illégale 14h",
        duree_cycle_jours=84,
        sequence_data=sequence_invalide
    )
    
    agent_kamikaze = AgentModel.objects.create(nom="Eve", date_debut_cycle=date_depart)
    
    # L'affectation doit échouer avec une ValidationError du moteur de conformité
    with pytest.raises(ValidationError) as excinfo:
        AffectationModel.objects.create(
            agent=agent_kamikaze, 
            trame=trame_invalide, 
            date_debut=date_depart
        )
    
    assert "RegleReposMinQuotidien" in str(excinfo.value)
    print("Test d'acceptance réussi : Couverture parfaite et règles légales respectées !")
