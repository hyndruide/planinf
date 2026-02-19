# app/applied_planning/models.py
from django.db import models
from uuid import uuid4

# Importation des modèles des autres Bounded Contexts
from resource_management.models import AgentModel
from pattern_engine.models import TrameModel

from .domain.affectation import Affectation

class AffectationModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    agent = models.ForeignKey(AgentModel, on_delete=models.CASCADE, related_name='affectations')
    trame = models.ForeignKey(TrameModel, on_delete=models.CASCADE, related_name='affectations')
    date_debut = models.DateField()

    class Meta:
        verbose_name = "Affectation"
        verbose_name_plural = "Affectations"
        unique_together = ('agent', 'trame', 'date_debut') # Un agent ne peut pas avoir la même trame à la même date de début

    def __str__(self):
        return f"Affectation de {self.agent.nom} à {self.trame.nom} débutant le {self.date_debut}"

    # Méthode pour convertir le modèle ORM en objet de domaine Affectation
    def to_domain(self) -> Affectation:
        return Affectation(
            id=self.id,
            agent_id=self.agent_id,
            trame_id=self.trame_id,
            date_debut=self.date_debut
        )

    # Méthode pour mettre à jour le modèle ORM à partir d'un objet de domaine Affectation
    @classmethod
    def from_domain(cls, affectation: Affectation) -> 'AffectationModel':
        try:
            instance = cls.objects.get(id=affectation.id)
            instance.agent_id = affectation.agent_id
            instance.trame_id = affectation.trame_id
            instance.date_debut = affectation.date_debut
        except cls.DoesNotExist:
            instance = cls(
                id=affectation.id,
                agent_id=affectation.agent_id,
                trame_id=affectation.trame_id,
                date_debut=affectation.date_debut
            )
        return instance
