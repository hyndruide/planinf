# app/solver_engine/services.py
from typing import List, Optional
from uuid import UUID
from datetime import date
from django.db import transaction

from resource_management.models import AgentModel
from demand_management.models import DailyRequirementModel
from compliance_engine.models import PolitiqueConformiteModel
from pattern_engine.models import TrameModel
from applied_planning.models import AffectationModel

from .domain.solver_service import ScheduleSolverService

def generate_and_save_schedule(
    agent_ids: List[UUID], 
    politique_id: UUID, 
    duree_cycle: int, 
    date_debut: date
) -> bool:
    """
    Orchestre la génération automatique du planning et persiste les résultats.
    """
    # 1. Préparation des données
    agents = [AgentModel.objects.get(id=aid).to_domain() for aid in agent_ids]
    requirements = [rm.to_domain() for rm in DailyRequirementModel.objects.all()]
    politique = PolitiqueConformiteModel.objects.get(id=politique_id).to_domain()
    
    # 2. Appel du solveur
    solver = ScheduleSolverService()
    result = solver.solve(agents, requirements, politique, duree_cycle)
    
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
