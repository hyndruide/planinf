# app/solver_engine/services.py
from typing import List, Optional
from uuid import UUID
from datetime import date, timedelta
from django.db import transaction

from resource_management.models import AgentModel
from demand_management.models import DailyRequirementModel
from compliance_engine.models import PolitiqueConformiteModel
from pattern_engine.models import TrameModel
from applied_planning.models import AffectationModel, AbsenceModel

from .domain.solver_service import ScheduleSolverService

def generate_and_save_schedule(
    agent_ids: List[UUID], 
    politique_ids: List[UUID], 
    duree_cycle: int, 
    date_debut: date
) -> bool:
    """
    Orchestre la génération automatique du planning et persiste les résultats.
    """
    # 1. Préparation des données
    agents = [AgentModel.objects.get(id=aid).to_domain() for aid in agent_ids]
    requirements = [rm.to_domain() for rm in DailyRequirementModel.objects.all()]
    politiques = [PolitiqueConformiteModel.objects.get(id=pid).to_domain() for pid in politique_ids]
    
    # Récupérer les absences sur la période pour ces agents
    date_fin = date_debut + timedelta(days=duree_cycle - 1)
    absences_models = AbsenceModel.objects.filter(
        agent_id__in=agent_ids,
        date_debut__lte=date_fin,
        date_fin__gte=date_debut
    )
    absences = [am.to_domain() for am in absences_models]
    
    # 2. Appel du solveur
    solver = ScheduleSolverService()
    result = solver.solve(
        agents, 
        requirements, 
        politiques, 
        duree_cycle,
        date_debut=date_debut,
        absences=absences
    )
    
    if not result:
        return False
        
    # 3. Persistance dans une transaction atomique
    with transaction.atomic():
        for agent_id, trame_domain in result.items():
            # Sauvegarde de la Trame
            trame_model = TrameModel.from_domain(trame_domain)
            trame_model.save()
            
            # Création de l'affectation
            agent_model = AgentModel.objects.get(id=agent_id)
            AffectationModel.objects.create(
                agent=agent_model,
                trame=trame_model,
                date_debut=date_debut
            )
            
    return True
