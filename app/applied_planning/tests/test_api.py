import pytest
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from resource_management.tests.factories import AgentFactory
from applied_planning.tests.factories import AffectationFactory
from pattern_engine.tests.factories import TrameFactory
from pattern_engine.domain.shift import Shift, ShiftType

@pytest.mark.django_db
def test_get_service_fte_report_api():
    client = APIClient()
    
    # Given
    agent1 = AgentFactory(nom="Agent 1", quotite=1.0)
    agent2 = AgentFactory(nom="Agent 2", quotite=0.5)
    
    # Trame : 35h par semaine (5*7h)
    trame = TrameFactory(
        duree_cycle_jours=7,
        sequence_data=[Shift(ShiftType.WORK, 7.0)]*5 + [Shift(ShiftType.REST, 0)]*2
    )
    
    # Affectations
    AffectationFactory(agent=agent1, trame=trame, date_debut=date(2026, 3, 1))
    AffectationFactory(agent=agent2, trame=trame, date_debut=date(2026, 3, 1))
    
    # When: Appel de l'API pour 1 semaine
    # Agent 1 fait 35h. Agent 2 fait 35h.
    # Total hours = 70h. Base Hebdo = 35h.
    # ETP Réel = 70 / 35 = 2.0
    # ETP Cible = 1.0 + 0.5 = 1.5
    response = client.get(
        '/api/v1/planning/reports/fte/', 
        {'start_date': '2026-03-01', 'end_date': '2026-03-07'}
    )
    
    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.data['fte_real'] == 2.0
    assert response.data['fte_target'] == 1.5
    assert response.data['num_agents'] == 2
