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
    result = solver.solve(agents, requirements, [politique], duree_cycle)
    
    # Then
    assert result is not None, "Le solveur aurait dû trouver une solution"
    assert len(result) == 4, "Chaque agent doit avoir une trame assignée"
    
    # Vérifier que les trames respectent la durée demandée
    for agent_id, trame in result.items():
        assert trame.duree_cycle_jours == duree_cycle
        assert len(trame.sequence) == duree_cycle

from compliance_engine.domain.regles import RegleHeuresMaxHebdo

def test_solver_respects_max_weekly_hours():
    # Given
    # 4 agents
    agents = [Agent(uuid4(), f"A{i}", Quotite(1.0), date(2026, 1, 1)) for i in range(4)]
    
    # Besoin : 2 agents par jour (14 shifts par semaine)
    requirements = [DailyRequirement(day, 2) for day in range(7)]
    
    # Règle stricte : Max 24h par semaine (soit 2 jours de 12h)
    # Avec 4 agents, on peut couvrir au max 4 * 2 = 8 shifts par semaine.
    # Or on en demande 14. C'est IMPOSSIBLE.
    politique = PolitiqueConformite(
        uuid4(), 
        "Stricte", 
        [RegleHeuresMaxHebdo(24)] 
    )
    
    solver = ScheduleSolverService()
    
    # When
    result = solver.solve(agents, requirements, [politique], 14)
    
    # Then
    # Grâce aux contraintes souples, le solveur trouve une solution légale
    # mais en sous-effectif (il ne planifie que ce qui est légalement possible).
    assert result is not None, "Le solveur doit retourner un planning (même en sous-effectif) plutôt que d'échouer"
    
    # Vérifions que la contrainte stricte est bien respectée : aucun agent ne dépasse 24h (2 shifts) sur 7 jours.
    for agent_id, trame in result.items():
        shifts_semaine_1 = sum(1 for s in trame.sequence[:7] if s.type.value == "WORK")
        assert shifts_semaine_1 * 12 <= 24, "La règle des heures max doit être respectée"

from compliance_engine.domain.regles import RegleReposDominical

def test_solver_respects_sunday_rest():
    # Given
    # 2 agents, 14 jours (2 dimanches)
    agents = [Agent(uuid4(), f"A{i}", Quotite(1.0), date(2026, 1, 1)) for i in range(2)]
    
    # Besoin : 1 agent par jour (7 jours sur 7)
    requirements = [DailyRequirement(day, 1) for day in range(7)]
    
    # Règle : REPOS obligatoire TOUS les dimanches (frequence=1 veut dire 1 repos sur 1 dimanche)
    # Attends, la règle dans regles.py dit : 
    # for i in range(0, len(sundays), self.frequence): 
    # batch = sundays[i:i+self.frequence]
    # has_rest = any(d.shift.type != ShiftType.WORK for d in batch)
    # if not has_rest: return False
    # Donc frequence=1 veut dire que chaque batch de 1 dimanche doit avoir un repos. 
    # Donc chaque dimanche est en repos.
    politique = PolitiqueConformite(
        uuid4(), 
        "PasDeDimanche", 
        [RegleReposDominical(1)] 
    )
    
    solver = ScheduleSolverService()
    
    # When
    result = solver.solve(agents, requirements, [politique], 14)
    
    # Then
    # On a besoin d'un agent le dimanche, mais la règle l'interdit.
    # Le solveur doit retourner un planning légal (personne le dimanche).
    assert result is not None, "Le solveur doit retourner un planning"
    
    for agent_id, trame in result.items():
        # Dimanche = index 6 et 13 (si Lundi = 0)
        assert trame.sequence[6].type.value == "REST", "Personne ne doit travailler le 1er dimanche"
        assert trame.sequence[13].type.value == "REST", "Personne ne doit travailler le 2ème dimanche"

from compliance_engine.domain.regles import RegleHeuresMaxJournalieres

def test_solver_fails_if_12h_shift_violates_daily_max():
    # Given
    agents = [Agent(uuid4(), "A1", Quotite(1.0), date(2026, 1, 1))]
    requirements = [DailyRequirement(0, 1)] # Lundi
    
    # Règle : Max 10h par jour
    # Or on travaille par shifts de 12h.
    politique = PolitiqueConformite(uuid4(), "Base", [RegleHeuresMaxJournalieres(10)])
    
    solver = ScheduleSolverService()
    
    # When
    result = solver.solve(agents, requirements, [politique], 7)
    
    # Then
    assert result is not None, "Le solveur doit retourner un planning vide car le shift dépasse la règle"
    
    # Vérifier que le planning est 100% vide
    for agent_id, trame in result.items():
        assert all(s.type.value == "REST" for s in trame.sequence), "Aucun agent ne doit travailler"
