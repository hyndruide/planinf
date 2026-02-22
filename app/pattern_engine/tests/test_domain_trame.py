# app/pattern_engine/tests/test_domain_trame.py
import pytest
from uuid import uuid4
from pattern_engine.domain.shift import Shift, ShiftType
from pattern_engine.domain.trame import Trame

def test_trame_get_shift_at_day_within_cycle():
    # Given
    shift_work = Shift(ShiftType.WORK, 12)
    shift_rest = Shift(ShiftType.REST, 0)
    sequence = [shift_work, shift_rest]
    trame = Trame(uuid4(), "Test Trame", 2, sequence)

    # When / Then
    assert trame.get_shift_at_day(0) == shift_work
    assert trame.get_shift_at_day(1) == shift_rest

def test_trame_get_shift_at_day_outside_cycle():
    # Given
    shift_work = Shift(ShiftType.WORK, 12)
    shift_rest = Shift(ShiftType.REST, 0)
    sequence = [shift_work, shift_rest]
    trame = Trame(uuid4(), "Test Trame", 2, sequence)

    # When / Then
    # Jour 2 (3ème jour) devrait correspondre au Jour 0
    assert trame.get_shift_at_day(2) == shift_work
    # Jour 3 devrait correspondre au Jour 1
    assert trame.get_shift_at_day(3) == shift_rest
    # Jour 10 devrait correspondre au Jour 0
    assert trame.get_shift_at_day(10) == shift_work

def test_trame_get_shift_at_day_negative_index():
    # Given
    shift_work = Shift(ShiftType.WORK, 12)
    shift_rest = Shift(ShiftType.REST, 0)
    sequence = [shift_work, shift_rest]
    trame = Trame(uuid4(), "Test Trame", 2, sequence)

    # When / Then
    # L'index ne devrait pas être négatif dans notre métier, mais le modulo Python gère ça.
    # On peut soit l'interdire, soit le tester. Testons le comportement actuel (modulo).
    assert trame.get_shift_at_day(-1) == shift_rest
