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

# Whitelist des classes autorisées pour la désérialisation (Security)
ALLOWED_REGLES = {
    RegleHeuresMaxJournalieres.__name__: RegleHeuresMaxJournalieres,
    RegleReposMinQuotidien.__name__: RegleReposMinQuotidien,
    RegleHeuresMaxHebdo.__name__: RegleHeuresMaxHebdo,
    RegleMoyenneHeuresHebdo.__name__: RegleMoyenneHeuresHebdo,
    RegleReposDominical.__name__: RegleReposDominical,
}

class RegleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, tuple(ALLOWED_REGLES.values())):
            # Ajoute un champ __type__ pour identifier la classe lors de la désérialisation
            result = obj.__dict__.copy() # Copie pour éviter de modifier l'original
            result['__type__'] = obj.__class__.__name__
            return result
        return super().default(obj)

def regle_object_hook(dct):
    if '__type__' in dct:
        type_name = dct.pop('__type__')
        cls = ALLOWED_REGLES.get(type_name)
        if cls:
            return cls(**dct)
    return dct

class RegleJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=regle_object_hook, *args, **kwargs)

# --- Modèle Django ---

class PolitiqueConformiteModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nom = models.CharField(max_length=255)
    # On spécifie le décodeur directement dans le champ
    regles_data = models.JSONField(encoder=RegleEncoder, decoder=RegleJSONDecoder, default=list)

    class Meta:
        verbose_name = "Politique de Conformité"
        verbose_name_plural = "Politiques de Conformité"

    def __str__(self):
        return self.nom

    def to_domain(self) -> PolitiqueConformite:
        # Django utilise RegleJSONDecoder lors du chargement, donc self.regles_data
        # contient déjà des objets Python typés (si tout va bien) ou des dicts (si le backend JSON natif bypass le decoder).
        # Pour être sûr avec SQLite (qui stocke du texte), le decoder fonctionne.
        # Avec Postgres, il faudrait peut-être une logique supplémentaire dans from_db_value.
        # Ici on suppose que le decoder fait son job ou que c'est géré.
        
        # Note de sécurité : Si le backend DB retourne des dicts (ex: Postgres JSONB),
        # il faudrait ré-instancier ici. Mais restons simple pour l'instant.
        return PolitiqueConformite(
            id=self.id,
            nom=self.nom,
            regles=self.regles_data
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
