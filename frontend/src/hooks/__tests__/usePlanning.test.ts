import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { usePlanning } from '../usePlanning';
import * as planningService from '../../services/planningService';
import { mockAgentPlanning, mockDayCoverage } from '../../mocks/planningData';
import type { GeneratePlanningPayload } from '../../types/planning';

// Mock the API service module
vi.mock('../../services/planningService');

describe('usePlanning Hook', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should initialize with default states', () => {
    const { result } = renderHook(() => usePlanning('2026-01-01', 2));

    expect(result.current.isLoading).toBe(false);
    expect(result.current.isGenerating).toBe(false);
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

  it('should handle errors gracefully during fetch', async () => {
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

  it('should handle generateSchedule and trigger refetch', async () => {
    const mockResponse = { message: 'Success' };
    vi.mocked(planningService.generatePlanning).mockResolvedValueOnce(mockResponse);
    vi.mocked(planningService.fetchFullPlanning).mockResolvedValueOnce(mockAgentPlanning);
    vi.mocked(planningService.fetchCoverageAnalysis).mockResolvedValueOnce(mockDayCoverage);

    const { result } = renderHook(() => usePlanning('2026-01-01', 2));
    
    const payload: GeneratePlanningPayload = {
      agent_ids: ['1', '2'],
      politique_id: 'pol-1',
      duree_cycle: 84,
      date_debut: '2026-01-01'
    };

    let response;
    await act(async () => {
      response = await result.current.generateSchedule(payload);
    });

    expect(response).toEqual(mockResponse);
    expect(result.current.isGenerating).toBe(false);
    // It should have refetched after generation
    expect(planningService.fetchFullPlanning).toHaveBeenCalledTimes(1);
    expect(result.current.planningData).toEqual(mockAgentPlanning);
  });

  it('should handle generateSchedule error', async () => {
    const errorMessage = 'Generation Error';
    vi.mocked(planningService.generatePlanning).mockRejectedValueOnce(new Error(errorMessage));

    const { result } = renderHook(() => usePlanning('2026-01-01', 2));
    
    const payload: GeneratePlanningPayload = {
      agent_ids: ['1', '2'],
      politique_id: 'pol-1',
      duree_cycle: 84,
      date_debut: '2026-01-01'
    };

    await act(async () => {
      await result.current.generateSchedule(payload);
    });

    expect(result.current.isGenerating).toBe(false);
    expect(result.current.error).toBe(`Erreur de génération : ${errorMessage}`);
    // Should not have refetched
    expect(planningService.fetchFullPlanning).toHaveBeenCalledTimes(0);
  });
});
