# app/pattern_engine/domain/shift.py
from enum import Enum

class ShiftType(Enum):
    WORK = "WORK"
    REST = "REST"
    ABSENCE = "ABSENCE"

class Shift:
    def __init__(self, type: ShiftType, duration: float, is_night: bool = False):
        if not isinstance(type, ShiftType):
            raise TypeError("Le type de shift doit être une instance de ShiftType.")
        if not isinstance(duration, (int, float)) or duration < 0:
            raise ValueError("La durée doit être un nombre non négatif.")
        if type == ShiftType.REST and duration != 0:
            raise ValueError("Un shift de type REST doit avoir une durée de 0.")
        if not isinstance(is_night, bool):
            raise TypeError("is_night doit être un booléen.")

        self._type = type
        self._duration = float(duration)
        self._is_night = is_night

    @property
    def type(self) -> ShiftType:
        return self._type

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def is_night(self) -> bool:
        return self._is_night

    def __eq__(self, other):
        if not isinstance(other, Shift):
            return NotImplemented
        return (self.type == other.type and 
                self.duration == other.duration and 
                self.is_night == other.is_night)

    def __hash__(self):
        return hash((self.type, self.duration, self.is_night))

    def __repr__(self):
        return f"Shift(type={self.type.name}, duration={self.duration}, is_night={self.is_night})"

    def __str__(self):
        night_str = " (Nuit)" if self.is_night else ""
        return f"{self.type.value} ({self.duration}h){night_str}"
