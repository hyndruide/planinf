import pytest
from rest_framework.test import APIClient
from rest_framework import status
from compliance_engine.models import PolitiqueConformiteModel
import json

@pytest.mark.django_db
def test_list_politiques():
    # Given
    client = APIClient()
    politique1 = PolitiqueConformiteModel.objects.create(
        nom="Politique Standard",
        regles_data=[
            {
                "__type__": "RegleReposMinQuotidien",
                "min_heures_repos": 11
            }
        ]
    )
    politique2 = PolitiqueConformiteModel.objects.create(
        nom="Politique Relax",
        regles_data=[]
    )

    # When
    response = client.get('/api/v1/compliance/politiques/')

    # Then
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert len(data) == 2
    
    # Check if the content is serialized properly
    noms = [p['nom'] for p in data]
    assert "Politique Standard" in noms
    assert "Politique Relax" in noms
    
    # Verify regles_data structure
    standard_pol = next(p for p in data if p['nom'] == "Politique Standard")
    assert isinstance(standard_pol['regles_data'], list)
    assert len(standard_pol['regles_data']) == 1
    assert standard_pol['regles_data'][0]['__type__'] == "RegleReposMinQuotidien"

from resource_management.tests.factories import AgentFactory
from applied_planning.tests.factories import AffectationFactory
from pattern_engine.tests.factories import TrameFactory
from pattern_engine.domain.shift import Shift, ShiftType
from datetime import date

@pytest.mark.django_db
def test_get_planning_audit_api():
    client = APIClient()
    
    # Given
    agent = AgentFactory(nom="Agent API Audit")
    trame = TrameFactory(
        duree_cycle_jours=7,
        sequence_data=[Shift(ShiftType.WORK, 12)]*5 + [Shift(ShiftType.REST, 0)]*2
    )
    AffectationFactory(agent=agent, trame=trame, date_debut=date(2026, 3, 1))
    
    # Règle restrictive: Max 48h (5*12 = 60h > 48h)
    politique = PolitiqueConformiteModel.objects.create(
        nom="Strict API",
        regles_data=[{"__type__": "RegleHeuresMaxHebdo", "max_heures": 48}]
    )
    
    # When
    response = client.get(
        '/api/v1/compliance/audit/', 
        {
            'agent_id': str(agent.id),
            'start_date': '2026-03-01',
            'end_date': '2026-03-07',
            'politique_ids': [str(politique.id)]
        }
    )
    
    # Then
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert len(data) == 7
    # 5ème jour (i=4) : 5*12=60h > 48h. Devrait être NC
    assert data[4]['is_compliant'] is False
    assert "Heures Max Hebdo" in [v['rule'] for v in data[4]['violations']]
