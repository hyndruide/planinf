# app/compliance_engine/domain/regles.py
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date
from pattern_engine.domain.services import PlannedDay
from pattern_engine.domain.shift import ShiftType

@dataclass(frozen=True)
class DailyComplianceStatus:
    date: date
    rule_name: str
    is_compliant: bool
    message: Optional[str] = None

@dataclass(frozen=True)
class RegleHeuresMaxJournalieres:
    max_heures: int

    def is_satisfied_by(self, planning: List[PlannedDay]) -> bool:
        return all(status.is_compliant for status in self.audit(planning))

    def audit(self, planning: List[PlannedDay]) -> List[DailyComplianceStatus]:
        results = []
        for day in planning:
            is_ok = True
            msg = None
            if day.shift.type == ShiftType.WORK and day.shift.duration > self.max_heures:
                is_ok = False
                msg = f"Dépassement du maximum journalier ({day.shift.duration}h > {self.max_heures}h)"
            
            results.append(DailyComplianceStatus(day.date, "Heures Max Journalières", is_ok, msg))
        return results

@dataclass(frozen=True)
class RegleReposMinQuotidien:
    min_heures_repos: int

    def is_satisfied_by(self, planning: List[PlannedDay]) -> bool:
        return all(status.is_compliant for status in self.audit(planning))

    def audit(self, planning: List[PlannedDay]) -> List[DailyComplianceStatus]:
        results = []
        # Simplification: on vérifie qu'aucun shift de travail + min_repos ne dépasse 24h.
        for day in planning:
            is_ok = True
            msg = None
            if day.shift.type == ShiftType.WORK and (24 - day.shift.duration) < self.min_heures_repos:
                is_ok = False
                msg = f"Repos quotidien insuffisant ({24 - day.shift.duration}h < {self.min_heures_repos}h)"
            
            results.append(DailyComplianceStatus(day.date, "Repos Min Quotidien", is_ok, msg))
        return results

@dataclass(frozen=True)
class RegleHeuresMaxHebdo:
    max_heures: int

    def is_satisfied_by(self, planning: List[PlannedDay]) -> bool:
        return all(status.is_compliant for status in self.audit(planning))

    def audit(self, planning: List[PlannedDay]) -> List[DailyComplianceStatus]:
        results = []
        if not planning:
            return results
            
        for i in range(len(planning)):
            day = planning[i]
            # Fenêtre de 7 jours glissants finissant aujourd'hui
            start_idx = max(0, i - 6)
            week = planning[start_idx : i + 1]
            total_hours = sum(d.shift.duration for d in week if d.shift.type == ShiftType.WORK)
            
            is_ok = True
            msg = None
            if total_hours > self.max_heures:
                is_ok = False
                msg = f"Dépassement du maximum hebdomadaire glissant ({total_hours}h > {self.max_heures}h)"
            
            results.append(DailyComplianceStatus(day.date, "Heures Max Hebdo", is_ok, msg))
        return results

@dataclass(frozen=True)
class RegleMoyenneHeuresHebdo:
    moyenne_heures: int
    periode_lissage_semaines: int

    def is_satisfied_by(self, planning: List[PlannedDay]) -> bool:
        return all(status.is_compliant for status in self.audit(planning))

    def audit(self, planning: List[PlannedDay]) -> List[DailyComplianceStatus]:
        results = []
        if not planning:
            return results
            
        total_hours = sum(d.shift.duration for d in planning if d.shift.type == ShiftType.WORK)
        nb_weeks = max(1, len(planning) / 7.0)
        actual_avg = total_hours / nb_weeks
        
        is_ok = actual_avg <= self.moyenne_heures
        msg = None if is_ok else f"Moyenne hebdomadaire ({actual_avg:.2f}h) > limite ({self.moyenne_heures}h)"
        
        # Pour une règle sur le cycle complet, on attache l'alerte au dernier jour du planning
        last_day = planning[-1]
        for day in planning:
            if day.date == last_day.date:
                results.append(DailyComplianceStatus(day.date, "Moyenne Heures Hebdo", is_ok, msg))
            else:
                results.append(DailyComplianceStatus(day.date, "Moyenne Heures Hebdo", True, None))
        return results

@dataclass(frozen=True)
class RegleReposDominical:
    frequence: int  # 1 dimanche sur `frequence`

    def is_satisfied_by(self, planning: List[PlannedDay]) -> bool:
        return all(status.is_compliant for status in self.audit(planning))

    def audit(self, planning: List[PlannedDay]) -> List[DailyComplianceStatus]:
        results = []
        sundays = [d for d in planning if d.date.weekday() == 6]
        if not sundays:
            return [DailyComplianceStatus(d.date, "Repos Dominical", True) for d in planning]
        
        # Identification des dimanches travaillés vs repos
        dimanches_ok = {}
        for i in range(0, len(sundays), self.frequence):
            batch = sundays[i : i + self.frequence]
            has_rest = any(d.shift.type != ShiftType.WORK for d in batch)
            for d in batch:
                dimanches_ok[d.date] = (has_rest, None if has_rest else f"Pas de dimanche en repos dans ce bloc de {self.frequence}")

        for day in planning:
            if day.date in dimanches_ok:
                is_ok, msg = dimanches_ok[day.date]
                results.append(DailyComplianceStatus(day.date, "Repos Dominical", is_ok, msg))
            else:
                results.append(DailyComplianceStatus(day.date, "Repos Dominical", True))
        return results
