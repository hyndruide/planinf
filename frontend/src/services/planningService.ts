import type { AgentPlanning, DayCoverage, GeneratePlanningPayload, GeneratePlanningResponse, Agent, Politique, DailyRequirementInput } from '../types/planning';
import { mockAgentPlanning, mockDayCoverage, mockAgents, mockPolitiques, mockDefaultRequirements } from '../mocks/planningData';

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

export const fetchAllAgents = async (): Promise<Agent[]> => {
  await delay(300);
  return mockAgents;
};

export const fetchAllPolitiques = async (): Promise<Politique[]> => {
  await delay(300);
  return mockPolitiques;
};

export const fetchDefaultRequirements = async (): Promise<DailyRequirementInput[]> => {
  await delay(300);
  return mockDefaultRequirements;
};

export const generatePlanning = async (
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  _payload: GeneratePlanningPayload
): Promise<GeneratePlanningResponse> => {
  // Simulate longer calculation for solver
  await delay(1500);
  return { message: 'Schedule generated successfully' };
};
