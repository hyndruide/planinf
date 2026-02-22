# app/solver_engine/tests/test_domain_solver.py
import pytest
from uuid import uuid4
from datetime import date
from resource_management.domain.agent import Agent
from resource_management.domain.quotite import Quotite
from demand_management.domain.requirement import DailyRequirement
from compliance_engine.domain.politique import PolitiqueConformite
from compliance_engine.domain.regles import RegleReposMinQuotidien

# L'import échouera tant que la classe n'est pas créée
from solver_engine.domain.solver_service import ScheduleSolverService

def test_solver_finds_optimal_schedule():
    # Given
    # 4 agents
    agents = [
        Agent(uuid4(), f"Agent {i}", Quotite(1.0), date(2026, 1, 1))
        for i in range(4)
    ]
    
    # Besoin : 2 agents par jour, tous les jours
    requirements = [DailyRequirement(day, 2) for day in range(7)]
    
    # Règle légale : 11h de repos min (donc max 13h de travail)
    politique = PolitiqueConformite(
        uuid4(), 
        "Base", 
        [RegleReposMinQuotidien(11)]
    )
    
    duree_cycle = 14 # Cycle de 14 jours
    
    solver = ScheduleSolverService()
    
    # When
    # Le solveur doit retourner un dictionnaire associant chaque UUID d'agent à une Trame générée
    result = solver.solve(agents, requirements, politique, duree_cycle)
    
    # Then
    assert result is not None, "Le solveur aurait dû trouver une solution"
    assert len(result) == 4, "Chaque agent doit avoir une trame assignée"
    
    # Vérifier que les trames respectent la durée demandée
    for agent_id, trame in result.items():
        assert trame.duree_cycle_jours == duree_cycle
        assert len(trame.sequence) == duree_cycle
