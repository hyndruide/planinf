# app/demand_management/tests/factories.py
import factory
from demand_management.models import DailyRequirementModel

class DailyRequirementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DailyRequirementModel
        django_get_or_create = ('day_of_week',)

    day_of_week = 0 # Lundi par défaut
    required_count = 2
