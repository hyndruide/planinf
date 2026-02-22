# app/demand_management/domain/services.py
from dataclasses import dataclass
from datetime import date
from typing import List, Dict
from .requirement import DailyRequirement
from pattern_engine.domain.services import PlannedDay
from pattern_engine.domain.shift import ShiftType

@dataclass(frozen=True)
class DayCoverage:
    date: date
    present_count: int
    required_count: int
    gap: int  # present_count - required_count

class CoverageService:
    def calculate_coverage(
        self, 
        projections: List[List[PlannedDay]], 
        requirements: List[DailyRequirement]
    ) -> List[DayCoverage]:
        """
        Calcule la couverture pour une période en comparant les projections de tous les agents
        avec les besoins quotidiens.
        """
        # 1. Créer un mapping pour un accès rapide aux besoins par jour de la semaine
        req_map = {r.day_of_week: r.required_count for r in requirements}
        
        # 2. Agréger les présences par date
        daily_presence: Dict[date, int] = {}
        
        for agent_planning in projections:
            for day in agent_planning:
                if day.shift.type == ShiftType.WORK:
                    daily_presence[day.date] = daily_presence.get(day.date, 0) + 1
                elif day.date not in daily_presence:
                    daily_presence[day.date] = 0

        # 3. Construire le rapport trié par date
        report = []
        for d in sorted(daily_presence.keys()):
            req = req_map.get(d.weekday(), 0) # weekday() : 0=Lundi
            present = daily_presence[d]
            report.append(DayCoverage(
                date=d,
                present_count=present,
                required_count=req,
                gap=present - req
            ))
            
        return report
