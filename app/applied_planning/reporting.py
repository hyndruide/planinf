from datetime import date
from typing import Dict, Any

from resource_management.models import AgentModel
from .services import get_agent_planning

def calculate_service_fte(start_date: date, end_date: date) -> Dict[str, Any]:
    """
    Calcule les ETP (Équivalent Temps Plein) réels et cibles pour un service.
    """
    agents = AgentModel.objects.all()
    num_days = (end_date - start_date).days + 1
    
    # Base légale hebdomadaire de 35h
    # Base pour la période = (35h / 7 jours) * nombre de jours
    base_period = (35.0 / 7.0) * num_days
    
    total_hours = 0.0
    total_night_hours = 0.0
    fte_target = 0.0
    
    for agent in agents:
        # ETP Cible basé sur le contrat
        fte_target += agent.quotite.value
        
        # Planning réel
        planning = get_agent_planning(agent.id, start_date, end_date)
        for day in planning:
            if day.shift.type.value == "WORK":
                total_hours += day.shift.duration
                if day.shift.is_night:
                    total_night_hours += day.shift.duration
                    
    # ETP Réel = Heures travaillées / Heures de la base légale sur la période
    fte_real = total_hours / base_period if base_period > 0 else 0.0
    
    return {
        "start_date": str(start_date),
        "end_date": str(end_date),
        "total_hours": total_hours,
        "total_night_hours": total_night_hours,
        "fte_target": round(fte_target, 2),
        "fte_real": round(fte_real, 2),
        "num_agents": agents.count()
    }
