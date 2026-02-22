# app/demand_management/domain/requirement.py
from dataclasses import dataclass

@dataclass(frozen=True)
class DailyRequirement:
    day_of_week: int  # 0 (Lundi) à 6 (Dimanche)
    required_count: int

    def __post_init__(self):
        if not (0 <= self.day_of_week <= 6):
            raise ValueError("Le jour de la semaine doit être compris entre 0 et 6.")
        if self.required_count < 0:
            raise ValueError("Le nombre d'agents requis ne peut pas être négatif.")
