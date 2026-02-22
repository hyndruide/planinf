import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchFullPlanning, fetchCoverageAnalysis } from '../planningService';
import { mockAgentPlanning, mockDayCoverage } from '../../mocks/planningData';

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
});
