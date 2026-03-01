import pytest
from rest_framework.test import APIClient
from rest_framework import status
from demand_management.models import DailyRequirementModel

@pytest.mark.django_db
def test_bulk_update_requirements():
    client = APIClient()
    
    # Prépare l'état initial : aucun besoin
    assert DailyRequirementModel.objects.count() == 0

    # Prépare le payload de bulk update (7 jours de la semaine)
    payload = [
        {"day_of_week": i, "required_count": 5} for i in range(7)
    ]
    
    # Cas 1 : Création (Bulk Insert)
    response = client.post('/api/v1/coverage/requirements/bulk/', payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert DailyRequirementModel.objects.count() == 7
    assert all(r.required_count == 5 for r in DailyRequirementModel.objects.all())

    # Cas 2 : Mise à jour (Bulk Update)
    payload_update = [
        {"day_of_week": i, "required_count": 10 if i < 5 else 2} for i in range(7)
    ]
    response = client.post('/api/v1/coverage/requirements/bulk/', payload_update, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert DailyRequirementModel.objects.count() == 7
    lundi = DailyRequirementModel.objects.get(day_of_week=0)
    dimanche = DailyRequirementModel.objects.get(day_of_week=6)
    assert lundi.required_count == 10
    assert dimanche.required_count == 2
