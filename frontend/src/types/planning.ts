export type ShiftType = 'WORK' | 'REST';

export interface Shift {
  type: ShiftType;
  duration: number;
}

export interface PlannedDay {
  date: string; // YYYY-MM-DD
  shift: Shift;
}

export interface AgentPlanning {
  agent_id: string;
  nom: string;
  planning: PlannedDay[];
}

export interface DayCoverage {
  date: string; // YYYY-MM-DD
  present_count: number;
  required_count: number;
  gap: number;
}

export interface GeneratePlanningPayload {
  agent_ids: string[];
  politique_id: string;
  duree_cycle: number;
  date_debut: string; // YYYY-MM-DD
}

export interface GeneratePlanningResponse {
  message: string;
}
