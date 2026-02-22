import type { AgentPlanning, DayCoverage, PlannedDay } from '../types/planning';

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
