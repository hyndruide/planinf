import type { AgentPlanning, DayCoverage, PlannedDay, Agent, Politique, DailyRequirementInput } from '../types/planning';

// Helper to generate dates
const generateDates = (startDate: string, days: number): string[] => {
  const dates = [];
  const start = new Date(startDate);
  for (let i = 0; i < days; i++) {
    const d = new Date(start);
    d.setDate(start.getDate() + i);
    dates.push(d.toISOString().split('T')[0]);
  }
  return dates;
};

const dates = generateDates('2026-01-01', 14);

// 2-2 cycle (2 days work, 2 days rest)
const cyclePattern = [
  { type: 'WORK', duration: 12 },
  { type: 'WORK', duration: 12 },
  { type: 'REST', duration: 0 },
  { type: 'REST', duration: 0 }
] as const;

// Helper to build planning for an agent
const buildPlanning = (offset: number): PlannedDay[] => {
  return dates.map((date, index) => {
    const cycleIndex = (index + offset) % 4;
    return {
      date,
      shift: { ...cyclePattern[cycleIndex] }
    };
  });
};

export const mockAgents: Agent[] = [
  { id: 'uuid-1', nom: 'Alice', quotite: 1.0 },
  { id: 'uuid-2', nom: 'Bob', quotite: 1.0 },
  { id: 'uuid-3', nom: 'Charlie', quotite: 0.8 },
  { id: 'uuid-4', nom: 'Diana', quotite: 1.0 },
  { id: 'uuid-5', nom: 'Eve', quotite: 0.5 },
];

export const mockPolitiques: Politique[] = [
  { id: 'pol-1', nom: 'Repos Standard (11h)' },
  { id: 'pol-2', nom: 'Repos Réduit (9h)' },
  { id: 'pol-3', nom: 'Cycle 12h Strict' },
];

export const mockDefaultRequirements: DailyRequirementInput[] = [
  { day: 'Lundi', count: 2 },
  { day: 'Mardi', count: 2 },
  { day: 'Mercredi', count: 2 },
  { day: 'Jeudi', count: 2 },
  { day: 'Vendredi', count: 2 },
  { day: 'Samedi', count: 1 },
  { day: 'Dimanche', count: 1 },
];

export const mockAgentPlanning: AgentPlanning[] = [
  {
    agent_id: 'uuid-1',
    nom: 'Alice',
    planning: buildPlanning(0) // Starts with WORK
  },
  {
    agent_id: 'uuid-2',
    nom: 'Bob',
    planning: buildPlanning(0) // Starts with WORK
  },
  {
    agent_id: 'uuid-3',
    nom: 'Charlie',
    planning: buildPlanning(2) // Starts with REST
  },
  {
    agent_id: 'uuid-4',
    nom: 'Diana',
    planning: buildPlanning(2) // Starts with REST
  }
];

// Calculate coverage dynamically based on the mock data
export const mockDayCoverage: DayCoverage[] = dates.map(date => {
  let presentCount = 0;
  mockAgentPlanning.forEach(agent => {
    const day = agent.planning.find(p => p.date === date);
    if (day && day.shift.type === 'WORK') {
      presentCount++;
    }
  });

  const requiredCount = 2; // Fixed requirement as per plan

  return {
    date,
    present_count: presentCount,
    required_count: requiredCount,
    gap: presentCount - requiredCount
  };
});
