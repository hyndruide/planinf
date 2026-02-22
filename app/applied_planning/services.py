# app/applied_planning/services.py
from uuid import UUID
from datetime import date
from typing import List
from .models import AffectationModel, AbsenceModel
from .domain.absence import Absence
from pattern_engine.domain.services import PlanningProjectionService, PlannedDay
from pattern_engine.domain.shift import Shift, ShiftType
from resource_management.models import AgentModel

def get_agent_planning(
    agent_id: UUID, 
    start_date: date, 
    end_date: date
) -> List[PlannedDay]:
    """
    Service applicatif pour récupérer le planning d'un agent sur une période donnée en intégrant les absences.
    """
    # 1. Récupération de l'affectation active pour cet agent
    try:
        affectation_model = AffectationModel.objects.filter(agent_id=agent_id).latest('date_debut')
    except AffectationModel.DoesNotExist:
        return []
    
    # 2. Conversion vers les objets de domaine
    affectation = affectation_model.to_domain()
    trame = affectation_model.trame.to_domain()
    
    # 3. Utilisation du service de domaine pour projeter le planning théorique
    projection_service = PlanningProjectionService()
    planning_theorique = projection_service.project_planning(
        trame=trame,
        pivot_date=affectation.date_debut,
        start_date=start_date,
        end_date=end_date
    )
    
    # 4. Récupérer les absences de l'agent sur la période
    absences = AbsenceModel.objects.filter(
        agent_id=agent_id,
        date_debut__lte=end_date,
        date_fin__gte=start_date
    )
    absences_domain = [a.to_domain() for a in absences]
    
    # 5. Surcharger la projection avec les absences
    planning_reel = []
    for day in planning_theorique:
        is_absent = False
        for absence in absences_domain:
            if absence.includes_date(day.date):
                is_absent = True
                break
        
        if is_absent:
            planning_reel.append(PlannedDay(date=day.date, shift=Shift(ShiftType.ABSENCE, 0)))
        else:
            planning_reel.append(day)
            
    return planning_reel

def find_replacements_for_absence(absence: Absence) -> List['Agent']:
    """
    Trouve des agents surnuméraires sur la même trame qui pourraient remplacer l'agent absent.
    """
    # Identifier la trame de l'agent absent
    try:
        absent_affectation = AffectationModel.objects.filter(agent_id=absence.agent_id).latest('date_debut')
    except AffectationModel.DoesNotExist:
        return []

    # Trouver tous les agents qui sont surnuméraires
    surnumeraires_models = AgentModel.objects.filter(est_surnumeraire=True)
    
    replacements = []
    for sur_model in surnumeraires_models:
        # Vérifier si le surnuméraire est sur la même trame
        sur_affectations = AffectationModel.objects.filter(agent_id=sur_model.id).order_by('-date_debut')
        if not sur_affectations.exists():
            continue
        
        sur_affectation = sur_affectations.first()
        if sur_affectation.trame_id != absent_affectation.trame_id:
            continue
            
        # Il faudrait idéalement vérifier si le surnuméraire est déjà utilisé ou en absence lui-même.
        # Pour le moment, on retourne tous les surnuméraires valides de la même trame.
        replacements.append(sur_model.to_domain())
        
    return replacements
