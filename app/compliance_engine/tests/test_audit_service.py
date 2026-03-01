import pytest
from datetime import date
from resource_management.tests.factories import AgentFactory
from applied_planning.tests.factories import AffectationFactory
from pattern_engine.tests.factories import TrameFactory
from pattern_engine.domain.shift import Shift, ShiftType
from compliance_engine.models import PolitiqueConformiteModel
from compliance_engine.services import run_planning_audit

@pytest.mark.django_db
def test_run_planning_audit_service():
    # Given: Un agent avec une règle de max 24h/hebdo
    agent = AgentFactory(nom="Agent Audit")
    # Un planning qui dépasse (3 shifts de 12h = 36h)
    trame = TrameFactory(
        duree_cycle_jours=7,
        sequence_data=[Shift(ShiftType.WORK, 12)]*3 + [Shift(ShiftType.REST, 0)]*4
    )
    # On crée l'affectation AVANT la politique pour que .save() passe
    AffectationFactory(agent=agent, trame=trame, date_debut=date(2026, 3, 1))
    
    politique = PolitiqueConformiteModel.objects.create(
        nom="Strict",
        regles_data=[{"__type__": "RegleHeuresMaxHebdo", "max_heures": 24}]
    )
    
    # When
    audit_report = run_planning_audit(
        agent_id=agent.id,
        start_date=date(2026, 3, 1),
        end_date=date(2026, 3, 7),
        politique_ids=[politique.id]
    )
    
    # Then
    # L'audit doit contenir 7 jours
    assert len(audit_report) == 7
    # Le 3ème jour de travail (3*12=36h > 24h) doit être NC
    # L'index 2 (3ème jour)
    day_3 = audit_report[2]
    assert day_3['is_compliant'] is False
    assert "Dépassement du maximum hebdomadaire" in day_3['message']
