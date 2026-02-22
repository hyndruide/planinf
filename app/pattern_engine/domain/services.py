# app/pattern_engine/domain/services.py
from dataclasses import dataclass
from datetime import date, timedelta
from typing import List
from .shift import Shift
from .trame import Trame

@dataclass(frozen=True)
class PlannedDay:
    date: date
    shift: Shift

class PlanningProjectionService:
    def project_planning(
        self, 
        trame: Trame, 
        pivot_date: date, 
        start_date: date, 
        end_date: date
    ) -> List[PlannedDay]:
        """
        Projette une trame sur une période donnée en fonction d'une date pivot.
        
        Args:
            trame: La trame théorique à projeter.
            pivot_date: La date de référence qui correspond au Jour 0 de la trame.
            start_date: La date de début de la projection souhaitée.
            end_date: La date de fin de la projection souhaitée.
        """
        if start_date > end_date:
            return []

        planning = []
        current_date = start_date
        
        while current_date <= end_date:
            # Calcul du décalage en jours par rapport à la date pivot
            delta = (current_date - pivot_date).days
            
            # Récupération du shift via l'index calculé (modulo géré par l'agrégat)
            shift = trame.get_shift_at_day(delta)
            
            planning.append(PlannedDay(date=current_date, shift=shift))
            current_date += timedelta(days=1)
            
        return planning
