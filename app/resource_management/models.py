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
    quotite = QuotiteField(default=1.0) # Ajout de la valeur par défaut
    date_debut_cycle = models.DateField()

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"

    def __str__(self):
        return self.nom

    # Méthode pour convertir le modèle ORM en objet de domaine Agent
    def to_domain(self) -> Agent:
        return Agent(
            id=self.id,
            nom=self.nom,
            quotite=self.quotite, # Correction: self.quotite est déjà un objet Quotite grâce à QuotiteField
            date_debut_cycle=self.date_debut_cycle
        )

    # Méthode pour mettre à jour le modèle ORM à partir d'un objet de domaine Agent
    @classmethod
    def from_domain(cls, agent: Agent) -> 'AgentModel':
        try:
            instance = cls.objects.get(id=agent.id)
            instance.nom = agent.nom
            instance.quotite = agent.quotite.value # Stocker la valeur float
            instance.date_debut_cycle = agent.date_debut_cycle
        except cls.DoesNotExist:
            instance = cls(
                id=agent.id,
                nom=agent.nom,
                quotite=agent.quotite.value, # Stocker la valeur float
                date_debut_cycle=agent.date_debut_cycle
            )
        return instance
