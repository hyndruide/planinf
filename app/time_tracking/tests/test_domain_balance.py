import pytest
from uuid import uuid4
from datetime import date, timedelta
from resource_management.domain.quotite import Quotite
from pattern_engine.domain.shift import Shift, ShiftType
from pattern_engine.domain.services import PlannedDay

# On supposera que ces classes vont être créées dans time_tracking.domain.balance
from time_tracking.domain.balance import TimeBalanceCalculator, ContractBase

def test_calculate_simple_weekly_balance():
    # Given: Un contrat de 35h à 100%
    base = ContractBase(hours_per_week=35.0, rtt_eligible=False)
    quotite = Quotite(1.0)
    
    # 3 shifts de 12h = 36h travaillées
    planning = [
        PlannedDay(date(2026, 3, 1) + timedelta(days=i), 
                   Shift(ShiftType.WORK, 12) if i < 3 else Shift(ShiftType.REST, 0))
        for i in range(7)
    ]
    
    calculator = TimeBalanceCalculator()
    
    # When
    report = calculator.calculate(planning, base, quotite)
    
    # Then
    # Balance attendue : 36h - 35h = +1h
    assert report.total_hours_worked == 36.0
    assert report.total_hours_due == 35.0
    assert report.balance == 1.0

def test_calculate_partial_time_balance():
    # Given: Un contrat de 35h à 80% (soit 28h dues par semaine)
    base = ContractBase(hours_per_week=35.0, rtt_eligible=False)
    quotite = Quotite(0.8)
    
    # 2 shifts de 12h = 24h travaillées
    planning = [
        PlannedDay(date(2026, 3, 1) + timedelta(days=i), 
                   Shift(ShiftType.WORK, 12) if i < 2 else Shift(ShiftType.REST, 0))
        for i in range(7)
    ]
    
    calculator = TimeBalanceCalculator()
    
    # When
    report = calculator.calculate(planning, base, quotite)
    
    # Then
    # Balance attendue : 24h - 28h = -4h
    assert report.total_hours_worked == 24.0
    assert report.total_hours_due == 28.0
    assert report.balance == -4.0
