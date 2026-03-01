import pytest
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from resource_management.tests.factories import AgentFactory
from applied_planning.tests.factories import AffectationFactory
from pattern_engine.tests.factories import TrameFactory
from pattern_engine.domain.shift import Shift, ShiftType

@pytest.mark.django_db
def test_get_agent_balance_api():
    client = APIClient()
    
    # Given
    agent = AgentFactory(nom="Agent API", quotite=1.0, base_horaire=35.0)
    shift_12 = Shift(ShiftType.WORK, 12)
    shift_rest = Shift(ShiftType.REST, 0)
    
    trame = TrameFactory(
        duree_cycle_jours=2,
        sequence_data=[shift_12, shift_rest]
    )
    
    AffectationFactory(agent=agent, trame=trame, date_debut=date(2026, 3, 1))
    
    # When: Appel de l'API pour 2 semaines (14 jours)
    # L'agent travaille 1 jour sur 2 (7 jours travaillés de 12h = 84h)
    # Base : 35h * 2 = 70h
    # Balance attendue : +14h
    response = client.get(
        f'/api/v1/time/balance/{agent.id}/', 
        {'start_date': '2026-03-01', 'end_date': '2026-03-14'}
    )
    
    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.data['balance'] == 14.0
    assert response.data['total_hours_worked'] == 84.0
