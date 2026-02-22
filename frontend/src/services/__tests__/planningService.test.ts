import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchFullPlanning, fetchCoverageAnalysis, generatePlanning, fetchAllAgents, fetchAllPolitiques, fetchDefaultRequirements } from '../planningService';
import { mockAgentPlanning, mockDayCoverage, mockAgents, mockPolitiques, mockDefaultRequirements } from '../../mocks/planningData';
import type { GeneratePlanningPayload } from '../../types/planning';

describe('Planning Service (Mocked API)', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('fetchFullPlanning should resolve with mock data after a delay', async () => {
    const promise = fetchFullPlanning('2026-01-01', 2);
    
    // Fast-forward time
    vi.advanceTimersByTime(500);
    
    const data = await promise;
    expect(data).toEqual(mockAgentPlanning);
  });

  it('fetchCoverageAnalysis should resolve with mock data after a delay', async () => {
    const promise = fetchCoverageAnalysis('2026-01-01', '2026-01-14');
    
    // Fast-forward time
    vi.advanceTimersByTime(500);
    
    const data = await promise;
    expect(data).toEqual(mockDayCoverage);
  });

  it('fetchAllAgents should resolve with mock agents after a delay', async () => {
    const promise = fetchAllAgents();
    vi.advanceTimersByTime(300);
    const data = await promise;
    expect(data).toEqual(mockAgents);
  });

  it('fetchAllPolitiques should resolve with mock politiques after a delay', async () => {
    const promise = fetchAllPolitiques();
    vi.advanceTimersByTime(300);
    const data = await promise;
    expect(data).toEqual(mockPolitiques);
  });

  it('fetchDefaultRequirements should resolve with mock requirements after a delay', async () => {
    const promise = fetchDefaultRequirements();
    vi.advanceTimersByTime(300);
    const data = await promise;
    expect(data).toEqual(mockDefaultRequirements);
  });

  it('generatePlanning should resolve with success message after a delay', async () => {
    const payload: GeneratePlanningPayload = {
      agent_ids: ['uuid-1', 'uuid-2'],
      politique_ids: ['pol-1'],
      duree_cycle: 84,
      date_debut: '2026-01-01'
    };

    const promise = generatePlanning(payload);
    
    // Fast-forward time
    vi.advanceTimersByTime(1500);
    
    const data = await promise;
    expect(data.message).toBe('Schedule generated successfully');
  });
});
