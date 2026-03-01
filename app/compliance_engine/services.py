from datetime import date
from uuid import UUID
from typing import List, Dict, Any

from .models import PolitiqueConformiteModel
from applied_planning.services import get_agent_planning

def run_planning_audit(
    agent_id: UUID, 
    start_date: date, 
    end_date: date, 
    politique_ids: List[UUID]
) -> List[Dict[str, Any]]:
    """
    Exécute l'audit de conformité sur un planning donné.
    Retourne une liste d'états de conformité par jour.
    """
    # 1. Chargement du planning
    planning = get_agent_planning(agent_id, start_date, end_date)
    
    # 2. Chargement des politiques
    politiques = [
        PolitiqueConformiteModel.objects.get(id=pid).to_domain() 
        for pid in politique_ids
    ]
    
    # 3. Exécution de l'audit pour chaque jour
    # On initialise un dictionnaire indexé par date pour fusionner les résultats
    audit_results_by_date = {}
    for day in planning:
        audit_results_by_date[day.date] = {
            "date": str(day.date),
            "is_compliant": True,
            "violations": [] # Liste des messages d'erreurs
        }
        
    for politique in politiques:
        for regle in politique.regles:
            # On appelle l'audit de la règle sur l'ensemble du planning
            daily_statuses = regle.audit(planning)
            for status in daily_statuses:
                if not status.is_compliant:
                    day_res = audit_results_by_date[status.date]
                    day_res["is_compliant"] = False
                    day_res["violations"].append({
                        "rule": status.rule_name,
                        "message": status.message
                    })
                    
    # 4. Formatage final (trié par date)
    sorted_dates = sorted(audit_results_by_date.keys())
    final_report = []
    for d in sorted_dates:
        res = audit_results_by_date[d]
        # On ajoute un message global pour simplifier le test
        res["message"] = "; ".join([v["message"] for v in res["violations"]])
        final_report.append(res)
        
    return final_report
