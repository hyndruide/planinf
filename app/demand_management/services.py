# app/demand_management/services.py
from datetime import date
from typing import List
from applied_planning.models import AffectationModel
from applied_planning.services import get_agent_planning
from .models import DailyRequirementModel
from .domain.services import CoverageService, DayCoverage

def get_coverage_analysis(start_date: date, end_date: date) -> List[DayCoverage]:
    """
    Récupère toutes les affectations actives, projette les plannings et compare au besoin.
    """
    # 1. Récupérer toutes les affectations qui se chevauchent avec la période
    # (Pour simplifier, on prend toutes les affectations actuelles)
    affectations = AffectationModel.objects.all()
    
    # 2. Générer les projections pour chaque agent
    all_projections = []
    for aff in affectations:
        planning = get_agent_planning(aff.agent_id, start_date, end_date)
        all_projections.append(planning)
        
    # 3. Récupérer les besoins définis
    requirements = [rm.to_domain() for rm in DailyRequirementModel.objects.all()]
    
    # 4. Calculer la couverture via le service de domaine
    service = CoverageService()
    return service.calculate_coverage(all_projections, requirements)
