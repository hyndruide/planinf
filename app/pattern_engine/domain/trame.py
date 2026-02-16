# app/pattern_engine/domain/trame.py
from uuid import UUID, uuid4
from typing import List
from .shift import Shift

class Trame:
    def __init__(self, id: UUID, nom: str, duree_cycle_jours: int, sequence: List[Shift]):
        if not isinstance(id, UUID):
            raise TypeError("L'ID doit être une instance de UUID.")
        if not nom or not isinstance(nom, str):
            raise ValueError("Le nom de la trame ne peut pas être vide et doit être une chaîne de caractères.")
        if not isinstance(duree_cycle_jours, int) or duree_cycle_jours <= 0:
            raise ValueError("La durée du cycle doit être un entier positif.")
        if not isinstance(sequence, list) or not all(isinstance(s, Shift) for s in sequence):
            raise TypeError("La séquence doit être une liste de Shifts.")
        if len(sequence) != duree_cycle_jours:
            raise ValueError("La longueur de la séquence doit correspondre à la durée du cycle.")

        self._id = id
        self._nom = nom
        self._duree_cycle_jours = duree_cycle_jours
        self._sequence = sequence

    @classmethod
    def create(cls, nom: str, duree_cycle_jours: int, sequence: List[Shift]) -> 'Trame':
        return cls(uuid4(), nom, duree_cycle_jours, sequence)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def duree_cycle_jours(self) -> int:
        return self._duree_cycle_jours

    @property
    def sequence(self) -> List[Shift]:
        return self._sequence

    def __eq__(self, other):
        if not isinstance(other, Trame):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"Trame(id={self.id}, nom='{self.nom}', duree_cycle_jours={self.duree_cycle_jours}, sequence={self.sequence})"
