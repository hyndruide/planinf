# app/applied_planning/models.py
from django.db import models
from uuid import uuid4

from resource_management.models import AgentModel
from pattern_engine.models import TrameModel

from .domain.affectation import Affectation
from .domain.absence import Absence, TypeAbsence

class AffectationModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    agent = models.ForeignKey(AgentModel, on_delete=models.CASCADE, related_name='affectations')
    trame = models.ForeignKey(TrameModel, on_delete=models.CASCADE, related_name='affectations')
    date_debut = models.DateField()

    class Meta:
        verbose_name = "Affectation"
        verbose_name_plural = "Affectations"
        unique_together = ('agent', 'trame', 'date_debut')

    def __str__(self):
        return f"Affectation de {self.agent.nom} à {self.trame.nom} débutant le {self.date_debut}"

    def clean(self):
        super().clean()
        from compliance_engine.models import PolitiqueConformiteModel
        from compliance_engine.domain.services import ValidationService
        from .services import get_agent_planning
        from datetime import timedelta

        # On simule sur 12 semaines (84 jours)
        end_date = self.date_debut + timedelta(days=84)
        
        # Le planning théorique (Attention: on utilise les services existants, 
        # il faudrait éviter une boucle infinie ou des imports circulaires. 
        # Simplification pour ce mock)
        from pattern_engine.domain.services import PlanningProjectionService
        projection_service = PlanningProjectionService()
        planning = projection_service.project_planning(
            trame=self.trame.to_domain(),
            pivot_date=self.date_debut,
            start_date=self.date_debut,
            end_date=end_date
        )

        politiques = PolitiqueConformiteModel.objects.all()
        if politiques.exists():
            politique = politiques.first().to_domain()
            validator = ValidationService()
            resultat = validator.validate_planning(planning, politique)
            
            if not resultat.est_conforme:
                from django.core.exceptions import ValidationError
                raise ValidationError(f"Non conforme: {resultat.details}")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def to_domain(self) -> Affectation:
        return Affectation(
            id=self.id,
            agent_id=self.agent_id,
            trame_id=self.trame_id,
            date_debut=self.date_debut
        )

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

class AbsenceModel(models.Model):
    TYPE_CHOICES = [
        ('MALADIE', 'Maladie'),
        ('CONGE_PAYE', 'Congé Payé'),
        ('FORMATION', 'Formation'),
        ('AUTRE', 'Autre'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    agent = models.ForeignKey(AgentModel, on_delete=models.CASCADE, related_name='absences')
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_absence = models.CharField(max_length=20, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "Absence"
        verbose_name_plural = "Absences"

    def __str__(self):
        return f"Absence de {self.agent.nom} du {self.date_debut} au {self.date_fin}"

    def to_domain(self) -> Absence:
        return Absence(
            id=self.id,
            agent_id=self.agent_id,
            date_debut=self.date_debut,
            date_fin=self.date_fin,
            type_absence=TypeAbsence(self.type_absence)
        )

    @classmethod
    def from_domain(cls, absence: Absence) -> 'AbsenceModel':
        try:
            instance = cls.objects.get(id=absence.id)
            instance.agent_id = absence.agent_id
            instance.date_debut = absence.date_debut
            instance.date_fin = absence.date_fin
            instance.type_absence = absence.type_absence.value
        except cls.DoesNotExist:
            instance = cls(
                id=absence.id,
                agent_id=absence.agent_id,
                date_debut=absence.date_debut,
                date_fin=absence.date_fin,
                type_absence=absence.type_absence.value
            )
        return instance
