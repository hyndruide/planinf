from datetime import date
from uuid import UUID
from typing import Dict, Any

from resource_management.models import AgentModel
from applied_planning.services import get_agent_planning
from .domain.balance import TimeBalanceCalculator, ContractBase

def calculate_agent_balance(agent_id: UUID, start_date: date, end_date: date) -> Dict[str, Any]:
    """
    Service applicatif pour calculer la balance horaire d'un agent.
    """
    # 1. Chargement de l'agent
    agent_model = AgentModel.objects.get(id=agent_id)
    agent_domain = agent_model.to_domain()
    
    # 2. Récupération du planning sur la période
    planning = get_agent_planning(agent_id, start_date, end_date)
    
    # 3. Préparation du contrat
    base = ContractBase(
        hours_per_week=agent_domain.base_horaire,
        rtt_eligible=agent_domain.rtt_eligible
    )
    
    # 4. Calcul de la balance
    calculator = TimeBalanceCalculator()
    report = calculator.calculate(planning, base, agent_domain.quotite)
    
    # 5. Retour sous forme de dictionnaire (prêt pour l'API)
    return {
        "agent_id": str(agent_id),
        "agent_nom": agent_domain.nom,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "total_hours_worked": report.total_hours_worked,
        "total_hours_due": report.total_hours_due,
        "balance": report.balance,
        "rtt_hours_earned": report.rtt_hours_earned
    }
