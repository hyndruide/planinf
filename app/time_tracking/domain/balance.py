from dataclasses import dataclass
from typing import List
from resource_management.domain.quotite import Quotite
from pattern_engine.domain.services import PlannedDay
from pattern_engine.domain.shift import ShiftType

@dataclass(frozen=True)
class ContractBase:
    hours_per_week: float
    rtt_eligible: bool

@dataclass(frozen=True)
class TimeBalanceReport:
    total_hours_worked: float
    total_hours_due: float
    balance: float
    rtt_hours_earned: float = 0.0

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
            if day.shift.type == ShiftType.WORK
        )
        
        # 2. Total des heures dues (en fonction de la durée du planning)
        if not planning:
            return TimeBalanceReport(0.0, 0.0, 0.0, 0.0)
            
        num_days = len(planning)
        num_weeks = num_days / 7.0
        
        # Heures dues = Base Hebdo * Quotité * nombre de semaines
        total_due = base.hours_per_week * quotite.value * num_weeks
        
        # 3. Calcul des RTT acquis
        rtt_earned = 0.0
        if base.rtt_eligible and base.hours_per_week > 35.0:
            rtt_per_week = base.hours_per_week - 35.0
            rtt_earned = rtt_per_week * quotite.value * num_weeks
            
        # 4. Balance finale
        balance = total_worked - total_due
        
        return TimeBalanceReport(
            total_hours_worked=float(total_worked),
            total_hours_due=float(total_due),
            balance=float(balance),
            rtt_hours_earned=float(rtt_earned)
        )
