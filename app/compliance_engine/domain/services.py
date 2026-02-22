# app/compliance_engine/domain/services.py
from dataclasses import dataclass
from typing import List, Optional
from pattern_engine.domain.services import PlannedDay
from .politique import PolitiqueConformite

@dataclass
class ResultatValidation:
    est_conforme: bool
    details: Optional[str] = None

class ValidationService:
    def validate_planning(self, planning: List[PlannedDay], politique: PolitiqueConformite) -> ResultatValidation:
        """
        Évalue toutes les règles d'une politique de conformité sur un planning donné.
        Retourne True si toutes les règles sont satisfaites, sinon False avec les détails.
        """
        for regle in politique.regles:
            if hasattr(regle, 'is_satisfied_by'):
                is_ok = regle.is_satisfied_by(planning)
                if not is_ok:
                    nom_regle = regle.__class__.__name__
                    return ResultatValidation(
                        est_conforme=False,
                        details=f"Violation de la règle: {nom_regle} avec {regle}"
                    )
        return ResultatValidation(est_conforme=True)
