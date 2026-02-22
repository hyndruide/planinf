# app/pattern_engine/tests/factories.py
import factory
from pattern_engine.models import TrameModel
from pattern_engine.domain.shift import Shift, ShiftType

class TrameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TrameModel

    nom = factory.Faker('word')
    duree_cycle_jours = 2
    sequence_data = [
        Shift(ShiftType.WORK, 12),
        Shift(ShiftType.REST, 0)
    ]
