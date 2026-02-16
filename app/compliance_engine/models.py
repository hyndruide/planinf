# app/compliance_engine/models.py
from django.db import models
from uuid import uuid4
import json
from .domain.politique import PolitiqueConformite
from .domain.regles import (
    RegleHeuresMaxJournalieres,
    RegleReposMinQuotidien,
    RegleHeuresMaxHebdo,
    RegleMoyenneHeuresHebdo,
    RegleReposDominical,
)

# --- Sérialisation/Désérialisation pour JSONField ---

class RegleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (
            RegleHeuresMaxJournalieres,
            RegleReposMinQuotidien,
            RegleHeuresMaxHebdo,
            RegleMoyenneHeuresHebdo,
            RegleReposDominical,
        )):
            # Ajoute un champ __type__ pour identifier la classe lors de la désérialisation
            result = obj.__dict__
            result['__type__'] = obj.__class__.__name__
            return result
        return super().default(obj)

def regle_decoder(obj):
    if '__type__' in obj:
        type_name = obj.pop('__type__')
        # Trouve la classe correspondante dans le module des règles
        cls = globals().get(type_name)
        if cls:
            return cls(**obj)
    return obj

# --- Modèle Django ---

class PolitiqueConformiteModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nom = models.CharField(max_length=255)
    regles_data = models.JSONField(encoder=RegleEncoder, default=list)

    class Meta:
        verbose_name = "Politique de Conformité"
        verbose_name_plural = "Politiques de Conformité"

    def __str__(self):
        return self.nom

    def to_domain(self) -> PolitiqueConformite:
        regles = json.loads(json.dumps(self.regles_data), object_hook=regle_decoder)
        return PolitiqueConformite(
            id=self.id,
            nom=self.nom,
            regles=regles
        )

    @classmethod
    def from_domain(cls, politique: PolitiqueConformite) -> 'PolitiqueConformiteModel':
        try:
            instance = cls.objects.get(id=politique.id)
            instance.nom = politique.nom
            instance.regles_data = politique.regles
        except cls.DoesNotExist:
            instance = cls(
                id=politique.id,
                nom=politique.nom,
                regles_data=politique.regles
            )
        return instance
