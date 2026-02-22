# app/compliance_engine/domain/regles.py
from dataclasses import dataclass
from typing import List
from pattern_engine.domain.services import PlannedDay
from pattern_engine.domain.shift import ShiftType

@dataclass(frozen=True)
class RegleHeuresMaxJournalieres:
    max_heures: int

    def is_satisfied_by(self, planning: List[PlannedDay]) -> bool:
        for day in planning:
            if day.shift.type == ShiftType.WORK and day.shift.duration > self.max_heures:
                return False
        return True

@dataclass(frozen=True)
class RegleReposMinQuotidien:
    min_heures_repos: int

    def is_satisfied_by(self, planning: List[PlannedDay]) -> bool:
        # Simplification: on vérifie qu'aucun shift de travail + min_repos ne dépasse 24h.
        for day in planning:
            if day.shift.type == ShiftType.WORK and (24 - day.shift.duration) < self.min_heures_repos:
                return False
        return True

@dataclass(frozen=True)
class RegleHeuresMaxHebdo:
    max_heures: int

    def is_satisfied_by(self, planning: List[PlannedDay]) -> bool:
        # Regroupe par semaine glissante de 7 jours (simplifié)
        if not planning:
            return True
        for i in range(len(planning) - 6):
            week = planning[i:i+7]
            total_hours = sum(d.shift.duration for d in week if d.shift.type == ShiftType.WORK)
            if total_hours > self.max_heures:
                return False
        return True

@dataclass(frozen=True)
class RegleMoyenneHeuresHebdo:
    moyenne_heures: int
    periode_lissage_semaines: int

    def is_satisfied_by(self, planning: List[PlannedDay]) -> bool:
        # Simplification
        if not planning:
            return True
        total_hours = sum(d.shift.duration for d in planning if d.shift.type == ShiftType.WORK)
        nb_weeks = max(1, len(planning) / 7)
        if (total_hours / nb_weeks) > self.moyenne_heures:
            return False
        return True

@dataclass(frozen=True)
class RegleReposDominical:
    frequence: int  # 1 dimanche sur `frequence`

    def is_satisfied_by(self, planning: List[PlannedDay]) -> bool:
        sundays = [d for d in planning if d.date.weekday() == 6]
        if not sundays:
            return True
        
        # On vérifie qu'au moins 1 dimanche sur 'frequence' est en repos
        for i in range(0, len(sundays), self.frequence):
            batch = sundays[i:i+self.frequence]
            if len(batch) == self.frequence:
                has_rest = any(d.shift.type != ShiftType.WORK for d in batch)
                if not has_rest:
                    return False
        return True
