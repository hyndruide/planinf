# app/pattern_engine/domain/shift.py
from enum import Enum

class ShiftType(Enum):
    WORK = "WORK"
    REST = "REST"

class Shift:
    def __init__(self, type: ShiftType, duration: int):
        if not isinstance(type, ShiftType):
            raise TypeError("Le type de shift doit être une instance de ShiftType.")
        if not isinstance(duration, int) or duration < 0:
            raise ValueError("La durée doit être un entier non négatif.")
        if type == ShiftType.REST and duration != 0:
            raise ValueError("Un shift de type REST doit avoir une durée de 0.")

        self._type = type
        self._duration = duration

    @property
    def type(self) -> ShiftType:
        return self._type

    @property
    def duration(self) -> int:
        return self._duration

    def __eq__(self, other):
        if not isinstance(other, Shift):
            return NotImplemented
        return self.type == other.type and self.duration == other.duration

    def __hash__(self):
        return hash((self.type, self.duration))

    def __repr__(self):
        return f"Shift(type={self.type.name}, duration={self.duration})"

    def __str__(self):
        return f"{self.type.value} ({self.duration}h)"
