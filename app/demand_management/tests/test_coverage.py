# app/demand_management/tests/test_coverage.py
import pytest
from datetime import date
from applied_planning.tests.factories import AffectationFactory
from demand_management.tests.factories import DailyRequirementFactory
from demand_management.services import get_coverage_analysis

@pytest.mark.django_db
def test_coverage_analysis_logic():
    # Given
    # 1. On définit un besoin de 2 agents pour le Lundi (index 0)
    DailyRequirementFactory(day_of_week=0, required_count=2)
    
    # 2. On crée 3 agents sur la même trame qui travaillent le Lundi
    # Trame par défaut de TrameFactory : [WORK, REST] (cycle de 2j)
    # Lundi 2026-02-16 (J0) -> WORK
    # Si on met la date de début au 2026-02-16 pour 3 agents, ils seront 3 présents.
    pivot_date = date(2026, 2, 16)
    for _ in range(3):
        AffectationFactory(date_debut=pivot_date)

    # When
    # Analyse pour le Lundi 2026-02-16
    report = get_coverage_analysis(pivot_date, pivot_date)

    # Then
    assert len(report) == 1
    analysis = report[0]
    assert analysis.date == pivot_date
    assert analysis.present_count == 3
    assert analysis.required_count == 2
    assert analysis.gap == 1 # Surplus de 1 agent
