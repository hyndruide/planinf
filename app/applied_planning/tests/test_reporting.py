import pytest
from datetime import date
from resource_management.tests.factories import AgentFactory
from applied_planning.tests.factories import AffectationFactory
from pattern_engine.tests.factories import TrameFactory
from pattern_engine.domain.shift import Shift, ShiftType
from applied_planning.reporting import calculate_service_fte

@pytest.mark.django_db
def test_calculate_service_fte():
    # Given: 2 agents travaillant chacun 35h par semaine (soit 70h à eux deux)
    # Sur un mois de 4 semaines, ils font 280h.
    # Base légale mensuelle : 151.67h
    # ETP attendu : 280 / 151.67 = ~1.85
    
    # On va tester sur une seule semaine pour simplifier
    # Semaine = 35h. ETP Hebdo = 35 / 35 = 1.0 (si on regarde juste 1 agent)
    
    agent = AgentFactory(nom="Agent FTE", quotite=1.0)
    # Trame : 35h par semaine (5*7h)
    trame = TrameFactory(
        duree_cycle_jours=7,
        sequence_data=[Shift(ShiftType.WORK, 7.0)]*5 + [Shift(ShiftType.REST, 0)]*2
    )
    AffectationFactory(agent=agent, trame=trame, date_debut=date(2026, 3, 1))
    
    # When
    fte_report = calculate_service_fte(
        start_date=date(2026, 3, 1),
        end_date=date(2026, 3, 7)
    )
    
    # Then
    # L'agent a travaillé 35h. Sur une semaine (base 35h), l'ETP réel est de 1.0.
    assert fte_report['total_hours'] == 35.0
    assert fte_report['fte_real'] == 1.0
    # On peut aussi sortir les ETP cibles (basés sur la quotité du contrat)
    assert fte_report['fte_target'] == 1.0
