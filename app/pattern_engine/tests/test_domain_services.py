# app/pattern_engine/tests/test_domain_services.py
import pytest
from datetime import date, timedelta
from uuid import uuid4
from pattern_engine.domain.shift import Shift, ShiftType
from pattern_engine.domain.trame import Trame
from pattern_engine.domain.services import PlanningProjectionService

def test_project_planning_success():
    # Given
    shift_work = Shift(ShiftType.WORK, 12)
    shift_rest = Shift(ShiftType.REST, 0)
    sequence = [shift_work, shift_rest] # Cycle de 2 jours
    trame = Trame(uuid4(), "Cycle 2j", 2, sequence)
    
    # Date pivot : Lundi 2026-02-16 (commence par WORK)
    pivot_date = date(2026, 2, 16)
    
    # On veut projeter du Lundi 2026-02-16 au Dimanche 2026-02-22 (7 jours)
    start_date = date(2026, 2, 16)
    end_date = date(2026, 2, 22)
    
    service = PlanningProjectionService()

    # When
    planning = service.project_planning(trame, pivot_date, start_date, end_date)

    # Then
    assert len(planning) == 7
    # Lun (J0): WORK
    assert planning[0].date == date(2026, 2, 16)
    assert planning[0].shift == shift_work
    # Mar (J1): REST
    assert planning[1].date == date(2026, 2, 17)
    assert planning[1].shift == shift_rest
    # Mer (J2): WORK
    assert planning[2].date == date(2026, 2, 18)
    assert planning[2].shift == shift_work

def test_project_planning_with_offset():
    # Given
    shift_work = Shift(ShiftType.WORK, 12)
    shift_rest = Shift(ShiftType.REST, 0)
    sequence = [shift_work, shift_rest]
    trame = Trame(uuid4(), "Cycle 2j", 2, sequence)
    
    # Pivot : Lundi 2026-02-16
    pivot_date = date(2026, 2, 16)
    
    # On veut projeter mais à partir de Mercredi 2026-02-18
    # Mercredi est à J2 du cycle par rapport à Lundi. J2 % 2 = 0 -> WORK
    start_date = date(2026, 2, 18)
    end_date = date(2026, 2, 18)
    
    service = PlanningProjectionService()

    # When
    planning = service.project_planning(trame, pivot_date, start_date, end_date)

    # Then
    assert len(planning) == 1
    assert planning[0].date == date(2026, 2, 18)
    assert planning[0].shift == shift_work
