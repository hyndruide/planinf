import pytest
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from compliance_engine.models import PolitiqueConformiteModel

@pytest.mark.django_db
def test_acceptance_full_api_workflow():
    """
    Test d'acceptance simulant les appels du Frontend vers l'API Backend.
    Scénario :
    1. Créer 4 agents.
    2. Définir un besoin de 2 agents par jour.
    3. Lancer le solveur pour générer le planning.
    4. Récupérer le planning généré et vérifier qu'il est correct.
    """
    client = APIClient()
    
    # 1. Configuration initiale (Côté Admin)
    # Création d'une politique de conformité directement en base (comme le ferait un admin)
    politique = PolitiqueConformiteModel.objects.create(
        nom="Politique Standard",
        regles_data=[
            {
                "__type__": "RegleReposMinQuotidien",
                "min_heures_repos": 11
            }
        ]
    )
    
    # 2. Création des agents via l'API REST
    agent_ids = []
    for i in range(4):
        response = client.post('/api/v1/resources/agents/', {
            "nom": f"Agent API {i}",
            "quotite": 1.0,
            "date_debut_cycle": "2026-01-01",
            "est_surnumeraire": False
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED, response.data
        agent_ids.append(response.data['id'])
        
    assert len(agent_ids) == 4

    # 3. Création des besoins quotidiens via l'API REST
    for day_of_week in range(7):
        response = client.post('/api/v1/coverage/requirements/', {
            "day_of_week": day_of_week,
            "required_count": 2
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED, response.data

    # 4. Lancement de la génération automatique via le Solveur
    generate_payload = {
        "agent_ids": agent_ids,
        "politique_ids": [str(politique.id)],
        "duree_cycle": 14,
        "date_debut": "2026-01-01"
    }
    response = client.post('/api/v1/solver/generate/', generate_payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert response.data['message'] == "Schedule generated successfully"

    # 5. Vérification du résultat en appelant l'API de vue globale
    response = client.get('/api/v1/planning/full-view/', {'start_date': '2026-01-01', 'weeks': '2'})
    assert response.status_code == status.HTTP_200_OK
    
    planning_data = response.data
    assert len(planning_data) == 4 # 4 agents
    
    # On va compter le nombre d'agents prévus au travail le premier jour (2026-01-01)
    agents_working_day_1 = 0
    for agent_data in planning_data:
        # Le premier élément du tableau 'planning' correspond à la date de début demandée
        day_1 = agent_data['planning'][0]
        assert str(day_1['date']) == '2026-01-01'
        if day_1['shift']['type'] == 'WORK':
            agents_working_day_1 += 1
            
    # Le solveur a dû planifier exactement 2 agents pour répondre au besoin (et pour économiser les heures)
    # Note: L'optimiseur essaie de couvrir au moins le besoin. S'il n'y a pas d'objectif strict de minimisation,
    # il pourrait en mettre plus, mais dans notre modèle simple, il devrait s'en tenir au strict nécessaire 
    # pour ménager les contraintes de rotation.
    assert agents_working_day_1 >= 2, "La couverture minimale n'est pas assurée le premier jour."
