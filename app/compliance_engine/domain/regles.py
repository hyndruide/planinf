# app/compliance_engine/domain/regles.py
from dataclasses import dataclass

@dataclass(frozen=True)
class RegleHeuresMaxJournalieres:
    max_heures: int

@dataclass(frozen=True)
class RegleReposMinQuotidien:
    min_heures_repos: int

@dataclass(frozen=True)
class RegleHeuresMaxHebdo:
    max_heures: int

@dataclass(frozen=True)
class RegleMoyenneHeuresHebdo:
    moyenne_heures: int
    periode_lissage_semaines: int

@dataclass(frozen=True)
class RegleReposDominical:
    frequence: int  # 1 dimanche sur `frequence`
