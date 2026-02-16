# app/resource_management/domain/agent.py
from uuid import UUID, uuid4
from datetime import date
from .quotite import Quotite

class Agent:
    def __init__(self, id: UUID, nom: str, quotite: Quotite, date_debut_cycle: date):
        if not isinstance(id, UUID):
            raise TypeError("L'ID doit être une instance de UUID.")
        if not nom or not isinstance(nom, str):
            raise ValueError("Le nom de l'agent ne peut pas être vide et doit être une chaîne de caractères.")
        if not isinstance(quotite, Quotite):
            raise TypeError("La quotité doit être une instance de Quotite.")
        if not isinstance(date_debut_cycle, date):
            raise TypeError("La date de début de cycle doit être une instance de date.")

        self._id = id
        self._nom = nom
        self._quotite = quotite
        self._date_debut_cycle = date_debut_cycle

    @classmethod
    def create(cls, nom: str, quotite: Quotite, date_debut_cycle: date) -> 'Agent':
        return cls(uuid4(), nom, quotite, date_debut_cycle)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def quotite(self) -> Quotite:
        return self._quotite

    @property
    def date_debut_cycle(self) -> date:
        return self._date_debut_cycle

    def __eq__(self, other):
        if not isinstance(other, Agent):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"Agent(id={self.id}, nom='{self.nom}', quotite={self.quotite}, date_debut_cycle={self.date_debut_cycle})"
