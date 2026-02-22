# app/applied_planning/tests/factories.py
import factory
from applied_planning.models import AffectationModel
from resource_management.tests.factories import AgentFactory
from pattern_engine.tests.factories import TrameFactory
from datetime import date

class AffectationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AffectationModel

    agent = factory.SubFactory(AgentFactory)
    trame = factory.SubFactory(TrameFactory)
    date_debut = factory.LazyFunction(date.today)
