# app/compliance_engine/domain/politique.py
from uuid import UUID, uuid4
from typing import List, Union
from .regles import (
    RegleHeuresMaxJournalieres,
    RegleReposMinQuotidien,
    RegleHeuresMaxHebdo,
    RegleMoyenneHeuresHebdo,
    RegleReposDominical,
)

# Type hint pour la liste des règles
ListeRegles = List[
    Union[
        RegleHeuresMaxJournalieres,
        RegleReposMinQuotidien,
        RegleHeuresMaxHebdo,
        RegleMoyenneHeuresHebdo,
        RegleReposDominical,
    ]
]

class PolitiqueConformite:
    def __init__(self, id: UUID, nom: str, regles: ListeRegles):
        if not isinstance(id, UUID):
            raise TypeError("L'ID doit être une instance de UUID.")
        if not nom or not isinstance(nom, str):
            raise ValueError("Le nom de la politique ne peut pas être vide et doit être une chaîne de caractères.")
        if not isinstance(regles, list):
            raise TypeError("Les règles doivent être fournies dans une liste.")

        self._id = id
        self._nom = nom
        self._regles = regles

    @classmethod
    def create(cls, nom: str, regles: ListeRegles) -> 'PolitiqueConformite':
        return cls(uuid4(), nom, regles)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def regles(self) -> ListeRegles:
        return self._regles

    def __eq__(self, other):
        if not isinstance(other, PolitiqueConformite):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"PolitiqueConformite(id={self.id}, nom='{self.nom}', regles={self.regles})"
