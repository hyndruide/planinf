# app/solver_engine/domain/solver_service.py
from typing import List, Dict, Optional
from uuid import UUID, uuid4
from ortools.sat.python import cp_model

from resource_management.domain.agent import Agent
from demand_management.domain.requirement import DailyRequirement
from compliance_engine.domain.politique import PolitiqueConformite
from pattern_engine.domain.trame import Trame
from pattern_engine.domain.shift import Shift, ShiftType

class ScheduleSolverService:
    def solve(
        self, 
        agents: List[Agent], 
        requirements: List[DailyRequirement], 
        politiques: List[PolitiqueConformite], 
        duree_cycle_jours: int
    ) -> Optional[Dict[UUID, Trame]]:
        """
        Génère les trames optimales pour un ensemble d'agents.
        """
        num_agents = len(agents)
        num_days = duree_cycle_jours
        
        # Mapping des besoins par jour de la semaine (0=Lundi, 6=Dimanche)
        req_map = {req.day_of_week: req.required_count for req in requirements}

        # 1. Initialisation du modèle
        model = cp_model.CpModel()

        # 2. Création des variables
        # work[a][d] = 1 si l'agent 'a' travaille le jour 'd', 0 sinon (repos)
        work = {}
        for a in range(num_agents):
            for d in range(num_days):
                work[(a, d)] = model.NewBoolVar(f'work_n{a}d{d}')

        # 3. Contraintes de couverture (Besoins Quotidiens)
        # Pour simplifier, on suppose que le jour 0 (d=0) est un Lundi (0)
        for d in range(num_days):
            day_of_week = d % 7
            req = req_map.get(day_of_week, 0)
            model.Add(sum(work[(a, d)] for a in range(num_agents)) >= req)

        # 4. Contraintes de Conformité Dynamiques
        from compliance_engine.domain.regles import RegleHeuresMaxHebdo, RegleReposDominical, RegleMoyenneHeuresHebdo, RegleHeuresMaxJournalieres, RegleReposMinQuotidien
        
        for politique in politiques:
            for regle in politique.regles:
                # RegleHeuresMaxJournalieres
                if isinstance(regle, RegleHeuresMaxJournalieres):
                    if regle.max_heures < 12:
                        # Impossible de travailler avec des shifts de 12h
                        for a in range(num_agents):
                            for d in range(num_days):
                                model.Add(work[(a, d)] == 0)

                # RegleReposMinQuotidien
                elif isinstance(regle, RegleReposMinQuotidien):
                    if (24 - 12) < regle.min_heures_repos:
                        # Impossible de travailler avec des shifts de 12h
                        for a in range(num_agents):
                            for d in range(num_days):
                                model.Add(work[(a, d)] == 0)

                # RegleHeuresMaxHebdo
                elif isinstance(regle, RegleHeuresMaxHebdo):
                    max_hours = regle.max_heures
                    for a in range(num_agents):
                        # On parcourt chaque fenêtre glissante de 7 jours
                        for d in range(num_days - 6):
                            model.Add(sum(work[(a, d+i)] * 12 for i in range(7)) <= max_hours)

                # RegleReposDominical
                elif isinstance(regle, RegleReposDominical):
                    freq = regle.frequence
                    for a in range(num_agents):
                        # On trouve les indices correspondant aux dimanches (d % 7 == 6 si d=0 est lundi)
                        dimanches = [d for d in range(num_days) if d % 7 == 6]
                        # On parcourt chaque fenêtre de N dimanches consécutifs
                        for i in range(len(dimanches) - freq + 1):
                            batch = dimanches[i : i + freq]
                            # Au moins un dimanche doit être REST (0)
                            model.Add(sum(work[(a, d)] for d in batch) <= freq - 1)

                # RegleMoyenneHeuresHebdo
                elif isinstance(regle, RegleMoyenneHeuresHebdo):
                    moyenne = regle.moyenne_heures
                    for a in range(num_agents):
                        # Somme totale <= moyenne * nb_semaines
                        # nb_semaines = num_days / 7
                        # Attention à utiliser des entiers avec OR-Tools
                        model.Add(sum(work[(a, d)] * 12 for d in range(num_days)) * 7 <= moyenne * num_days)

        # 5. Objectif : Répartition équitable des jours de travail
        # Minimiser la différence de jours travaillés entre le max et le min
        total_shifts_per_agent = [sum(work[(a, d)] for d in range(num_days)) for a in range(num_agents)]
        min_shifts = model.NewIntVar(0, num_days, 'min_shifts')
        max_shifts = model.NewIntVar(0, num_days, 'max_shifts')
        model.AddMinEquality(min_shifts, total_shifts_per_agent)
        model.AddMaxEquality(max_shifts, total_shifts_per_agent)
        
        # On minimise l'écart entre celui qui travaille le plus et celui qui travaille le moins
        model.Minimize(max_shifts - min_shifts)

        # 6. Résolution
        solver = cp_model.CpSolver()
        # Limite de temps pour ne pas bloquer indéfiniment
        solver.parameters.max_time_in_seconds = 10.0 
        status = solver.Solve(model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            # 7. Extraction des résultats et création des Trames
            result: Dict[UUID, Trame] = {}
            for a in range(num_agents):
                agent = agents[a]
                sequence = []
                for d in range(num_days):
                    is_working = solver.Value(work[(a, d)])
                    if is_working:
                        sequence.append(Shift(ShiftType.WORK, 12))
                    else:
                        sequence.append(Shift(ShiftType.REST, 0))
                
                # Création d'une trame unique pour cet agent
                trame = Trame(
                    id=uuid4(),
                    nom=f"Trame générée pour {agent.nom}",
                    duree_cycle_jours=duree_cycle_jours,
                    sequence=sequence
                )
                result[agent.id] = trame
                
            return result
        else:
            # Aucune solution trouvée
            return None
