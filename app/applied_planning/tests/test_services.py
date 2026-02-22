# app/applied_planning/tests/test_services.py
import pytest
from datetime import date
from applied_planning.tests.factories import AffectationFactory
from applied_planning.services import get_agent_planning
from pattern_engine.domain.shift import ShiftType

@pytest.mark.django_db
def test_get_agent_planning_integration():
    # Given
    # Création d'une affectation via factory (crée aussi Agent et Trame)
    # Trame par défaut : [WORK(12h), REST(0h)]
    # Date début affectation par défaut : aujourd'hui
    affectation = AffectationFactory(date_debut=date(2026, 2, 16))
    agent_id = affectation.agent.id
    
    # On demande le planning pour le premier jour (devrait être WORK)
    start_date = date(2026, 2, 16)
    end_date = date(2026, 2, 16)

    # When
    planning = get_agent_planning(agent_id, start_date, end_date)

    # Then
    assert len(planning) == 1
    assert planning[0].date == date(2026, 2, 16)
    assert planning[0].shift.type == ShiftType.WORK
    assert planning[0].shift.duration == 12
