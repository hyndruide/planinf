# app/resource_management/domain/quotite.py
import uuid

class Quotite:
    def __init__(self, value: float):
        if not (0 <= value <= 1):
            raise ValueError("La quotité doit être comprise entre 0 et 1.")
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    def __eq__(self, other):
        if not isinstance(other, Quotite):
            return NotImplemented
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return f"Quotite({self.value})"

    def __str__(self):
        return f"{int(self.value * 100)}%"
