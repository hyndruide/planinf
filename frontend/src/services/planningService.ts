import type { AgentPlanning, DayCoverage } from '../types/planning';
import { mockAgentPlanning, mockDayCoverage } from '../mocks/planningData';

// Simulated network delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const fetchFullPlanning = async (
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  _startDate: string,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  _weeks?: number
): Promise<AgentPlanning[]> => {
  await delay(500);
  return mockAgentPlanning;
};

export const fetchCoverageAnalysis = async (
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  _startDate: string,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  _endDate: string
): Promise<DayCoverage[]> => {
  await delay(500);
  return mockDayCoverage;
};
