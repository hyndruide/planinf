# app/demand_management/models.py
from django.db import models
from .domain.requirement import DailyRequirement

class DailyRequirementModel(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    ]
    
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, unique=True)
    required_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Besoin Quotidien"
        verbose_name_plural = "Besoins Quotidiens"

    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.required_count} agents"

    def to_domain(self) -> DailyRequirement:
        return DailyRequirement(
            day_of_week=self.day_of_week,
            required_count=self.required_count
        )
