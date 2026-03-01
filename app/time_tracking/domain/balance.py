from dataclasses import dataclass
from typing import List
from resource_management.domain.quotite import Quotite
from pattern_engine.domain.services import PlannedDay

@dataclass(frozen=True)
class ContractBase:
    hours_per_week: float
    rtt_eligible: bool

@dataclass(frozen=True)
class TimeBalanceReport:
    total_hours_worked: float
    total_hours_due: float
    balance: float

class TimeBalanceCalculator:
    def calculate(
        self, 
        planning: List[PlannedDay], 
        base: ContractBase, 
        quotite: Quotite
    ) -> TimeBalanceReport:
        """
        Calcule la balance horaire d'un agent sur une période donnée.
        """
        # 1. Total des heures travaillées
        total_worked = sum(
            day.shift.duration for day in planning 
            if day.shift.type.value == "WORK"
        )
        
        # 2. Total des heures dues (en fonction de la durée du planning)
        # On calcule le nombre de semaines (même partielles) couvertes
        if not planning:
            return TimeBalanceReport(0.0, 0.0, 0.0)
            
        # Simplification: on prend la durée totale du planning en jours / 7
        num_days = len(planning)
        num_weeks = num_days / 7.0
        
        # Heures dues = Base Hebdo * Quotité * nombre de semaines
        total_due = base.hours_per_week * quotite.value * num_weeks
        
        # 3. Balance finale
        balance = total_worked - total_due
        
        return TimeBalanceReport(
            total_hours_worked=float(total_worked),
            total_hours_due=float(total_due),
            balance=float(balance)
        )
