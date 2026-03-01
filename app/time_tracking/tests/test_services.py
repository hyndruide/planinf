import pytest
from datetime import date
from resource_management.tests.factories import AgentFactory
from applied_planning.tests.factories import AffectationFactory
from pattern_engine.tests.factories import TrameFactory
from pattern_engine.domain.shift import Shift, ShiftType
from time_tracking.services import calculate_agent_balance

@pytest.mark.django_db
def test_calculate_agent_balance_service():
    # Given: Un agent à 100% sur base 37.5h (RTT eligible)
    agent = AgentFactory(
        nom="Test Agent", 
        quotite=1.0, 
        base_horaire=37.5, 
        rtt_eligible=True
    )
    
    # Une trame simple : 5 jours de 7.5h suivis de 2 jours de repos
    shift_75 = Shift(ShiftType.WORK, 7.5)
    shift_rest = Shift(ShiftType.REST, 0)
    
    trame = TrameFactory(
        duree_cycle_jours=7,
        sequence_data=[shift_75]*5 + [shift_rest]*2
    )
    
    # Affectation de l'agent à cette trame
    AffectationFactory(agent=agent, trame=trame, date_debut=date(2026, 3, 1))
    
    # When: Calcul de la balance pour la première semaine
    report = calculate_agent_balance(
        agent_id=agent.id, 
        start_date=date(2026, 3, 1), 
        end_date=date(2026, 3, 7)
    )
    
    # Then
    assert report['total_hours_worked'] == 37.5
    assert report['balance'] == 0.0
    assert report['rtt_hours_earned'] == 2.5
