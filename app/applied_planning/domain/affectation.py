# app/applied_planning/domain/affectation.py
from uuid import UUID, uuid4
from datetime import date

class Affectation:
    def __init__(self, id: UUID, agent_id: UUID, trame_id: UUID, date_debut: date):
        if not isinstance(id, UUID):
            raise TypeError("L'ID doit être une instance de UUID.")
        if not isinstance(agent_id, UUID):
            raise TypeError("L'agent_id doit être une instance de UUID.")
        if not isinstance(trame_id, UUID):
            raise TypeError("La trame_id doit être une instance de UUID.")
        if not isinstance(date_debut, date):
            raise ValueError("La date de début doit être une instance de date.")

        self._id = id
        self._agent_id = agent_id
        self._trame_id = trame_id
        self._date_debut = date_debut

    @classmethod
    def create(cls, agent_id: UUID, trame_id: UUID, date_debut: date) -> 'Affectation':
        return cls(uuid4(), agent_id, trame_id, date_debut)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def agent_id(self) -> UUID:
        return self._agent_id

    @property
    def trame_id(self) -> UUID:
        return self._trame_id

    @property
    def date_debut(self) -> date:
        return self._date_debut

    def __eq__(self, other):
        if not isinstance(other, Affectation):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"Affectation(id={self.id}, agent_id={self.agent_id}, trame_id={self.trame_id}, date_debut={self.date_debut})"
