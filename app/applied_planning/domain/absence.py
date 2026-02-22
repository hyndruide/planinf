# app/applied_planning/domain/absence.py
from uuid import UUID, uuid4
from datetime import date
from enum import Enum

class TypeAbsence(Enum):
    MALADIE = "MALADIE"
    CONGE_PAYE = "CONGE_PAYE"
    FORMATION = "FORMATION"
    AUTRE = "AUTRE"

class Absence:
    def __init__(self, id: UUID, agent_id: UUID, date_debut: date, date_fin: date, type_absence: TypeAbsence):
        if not isinstance(id, UUID):
            raise TypeError("L'ID doit être une instance de UUID.")
        if not isinstance(agent_id, UUID):
            raise TypeError("L'agent_id doit être une instance de UUID.")
        if not isinstance(date_debut, date):
            raise TypeError("La date de début doit être une instance de date.")
        if not isinstance(date_fin, date):
            raise TypeError("La date de fin doit être une instance de date.")
        if not isinstance(type_absence, TypeAbsence):
            raise TypeError("Le type d'absence doit être une instance de TypeAbsence.")
        if date_debut > date_fin:
            raise ValueError("La date de début ne peut pas être postérieure à la date de fin.")

        self._id = id
        self._agent_id = agent_id
        self._date_debut = date_debut
        self._date_fin = date_fin
        self._type_absence = type_absence

    @classmethod
    def create(cls, agent_id: UUID, date_debut: date, date_fin: date, type_absence: TypeAbsence) -> 'Absence':
        return cls(uuid4(), agent_id, date_debut, date_fin, type_absence)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def agent_id(self) -> UUID:
        return self._agent_id

    @property
    def date_debut(self) -> date:
        return self._date_debut

    @property
    def date_fin(self) -> date:
        return self._date_fin

    @property
    def type_absence(self) -> TypeAbsence:
        return self._type_absence

    def includes_date(self, target_date: date) -> bool:
        return self.date_debut <= target_date <= self.date_fin

    def __eq__(self, other):
        if not isinstance(other, Absence):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"Absence(id={self.id}, agent_id={self.agent_id}, date_debut={self.date_debut}, date_fin={self.date_fin}, type={self.type_absence.name})"
