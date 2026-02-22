# app/pattern_engine/models.py
from django.db import models
from uuid import uuid4
import json
from .domain.shift import Shift, ShiftType
from .domain.trame import Trame
from django.core.serializers.json import DjangoJSONEncoder

class ShiftEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ShiftType):
            return obj.value
        if isinstance(obj, Shift):
            return {'type': obj.type.value, 'duration': obj.duration}
        return super().default(obj)

def shift_decoder(obj):
    if 'type' in obj and 'duration' in obj:
        return Shift(ShiftType(obj['type']), obj['duration'])
    return obj

class TrameModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nom = models.CharField(max_length=255)
    duree_cycle_jours = models.IntegerField()
    # Utilisation de JSONField pour stocker la séquence de Shift
    sequence_data = models.JSONField(encoder=ShiftEncoder, default=list)

    class Meta:
        verbose_name = "Trame"
        verbose_name_plural = "Trames"

    def __str__(self):
        return self.nom

    # Méthode pour convertir le modèle ORM en objet de domaine Trame
    def to_domain(self) -> Trame:
        # sequence_data peut être une liste de dicts si récupéré de la DB
        # On s'assure que chaque élément est un objet Shift
        sequence = []
        for item in self.sequence_data:
            if isinstance(item, dict):
                sequence.append(shift_decoder(item))
            else:
                sequence.append(item)
        
        return Trame(
            id=self.id,
            nom=self.nom,
            duree_cycle_jours=self.duree_cycle_jours,
            sequence=sequence
        )

    # Méthode pour mettre à jour le modèle ORM à partir d'un objet de domaine Trame
    @classmethod
    def from_domain(cls, trame: Trame) -> 'TrameModel':
        try:
            instance = cls.objects.get(id=trame.id)
            instance.nom = trame.nom
            instance.duree_cycle_jours = trame.duree_cycle_jours
            instance.sequence_data = trame.sequence # sequence_data sera encodé par ShiftEncoder
        except cls.DoesNotExist:
            instance = cls(
                id=trame.id,
                nom=trame.nom,
                duree_cycle_jours=trame.duree_cycle_jours,
                sequence_data=trame.sequence # sequence_data sera encodé par ShiftEncoder
            )
        return instance
