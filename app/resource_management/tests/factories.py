# app/resource_management/tests/factories.py
import factory
from resource_management.models import AgentModel
from datetime import date

class AgentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AgentModel

    nom = factory.Faker('name')
    quotite = 1.0
    date_debut_cycle = factory.LazyFunction(date.today)
