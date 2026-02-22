import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { usePlanning } from '../usePlanning';
import * as planningService from '../../services/planningService';
import { mockAgentPlanning, mockDayCoverage } from '../../mocks/planningData';

// Mock the API service module
vi.mock('../../services/planningService');

describe('usePlanning Hook', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should initialize with default states', () => {
    const { result } = renderHook(() => usePlanning('2026-01-01', 2));

    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(result.current.planningData).toEqual([]);
    expect(result.current.coverageData).toEqual([]);
  });

  it('should fetch and update state correctly', async () => {
    // Setup mock responses
    vi.mocked(planningService.fetchFullPlanning).mockResolvedValueOnce(mockAgentPlanning);
    vi.mocked(planningService.fetchCoverageAnalysis).mockResolvedValueOnce(mockDayCoverage);

    const { result } = renderHook(() => usePlanning('2026-01-01', 2));

    expect(result.current.isLoading).toBe(false);

    // Trigger the fetch within act
    await act(async () => {
      await result.current.triggerFetch();
    });

    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(result.current.planningData).toEqual(mockAgentPlanning);
    expect(result.current.coverageData).toEqual(mockDayCoverage);
    
    expect(planningService.fetchFullPlanning).toHaveBeenCalledWith('2026-01-01', 2);
    expect(planningService.fetchCoverageAnalysis).toHaveBeenCalledWith('2026-01-01', '2026-01-14'); // 2 weeks
  });

  it('should handle errors gracefully', async () => {
    const errorMessage = 'Network Error';
    vi.mocked(planningService.fetchFullPlanning).mockRejectedValueOnce(new Error(errorMessage));
    vi.mocked(planningService.fetchCoverageAnalysis).mockResolvedValueOnce(mockDayCoverage);

    const { result } = renderHook(() => usePlanning('2026-01-01', 2));

    await act(async () => {
      await result.current.triggerFetch();
    });

    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe(errorMessage);
    expect(result.current.planningData).toEqual([]);
    expect(result.current.coverageData).toEqual([]);
  });
});
