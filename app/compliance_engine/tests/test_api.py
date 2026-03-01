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
