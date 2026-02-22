# app/resource_management/models.py
from django.db import models
from uuid import uuid4
from .domain.quotite import Quotite
from .domain.agent import Agent

# Custom field for Quotite Value Object
class QuotiteField(models.FloatField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return Quotite(value)

    def to_python(self, value):
        if isinstance(value, Quotite):
            return value
        if value is None:
            return value
        return Quotite(value)

    def get_prep_value(self, value):
        if isinstance(value, Quotite):
            return value.value
        return value

class AgentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nom = models.CharField(max_length=255)
    quotite = QuotiteField(default=1.0)
    date_debut_cycle = models.DateField()
    est_surnumeraire = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"

    def __str__(self):
        return self.nom

    def to_domain(self) -> Agent:
        return Agent(
            id=self.id,
            nom=self.nom,
            quotite=self.quotite,
            date_debut_cycle=self.date_debut_cycle,
            est_surnumeraire=self.est_surnumeraire
        )

    @classmethod
    def from_domain(cls, agent: Agent) -> 'AgentModel':
        try:
            instance = cls.objects.get(id=agent.id)
            instance.nom = agent.nom
            instance.quotite = agent.quotite.value
            instance.date_debut_cycle = agent.date_debut_cycle
            instance.est_surnumeraire = agent.est_surnumeraire
        except cls.DoesNotExist:
            instance = cls(
                id=agent.id,
                nom=agent.nom,
                quotite=agent.quotite.value,
                date_debut_cycle=agent.date_debut_cycle,
                est_surnumeraire=agent.est_surnumeraire
            )
        return instance
