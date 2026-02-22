import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useConfiguration } from '../useConfiguration';
import * as planningService from '../../services/planningService';
import { mockAgents, mockPolitiques, mockDefaultRequirements } from '../../mocks/planningData';

vi.mock('../../services/planningService');

describe('useConfiguration Hook', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should initialize with default states', () => {
    const { result } = renderHook(() => useConfiguration());

    expect(result.current.isLoading).toBe(true); // Should start loading immediately in useEffect
    expect(result.current.agents).toEqual([]);
    expect(result.current.politiques).toEqual([]);
    expect(result.current.defaultRequirements).toEqual([]);
    expect(result.current.error).toBeNull();
  });

  it('should fetch configuration data on mount', async () => {
    vi.mocked(planningService.fetchAllAgents).mockResolvedValueOnce(mockAgents);
    vi.mocked(planningService.fetchAllPolitiques).mockResolvedValueOnce(mockPolitiques);
    vi.mocked(planningService.fetchDefaultRequirements).mockResolvedValueOnce(mockDefaultRequirements);

    const { result } = renderHook(() => useConfiguration());

    await waitFor(() => expect(result.current.isLoading).toBe(false));

    expect(result.current.agents).toEqual(mockAgents);
    expect(result.current.politiques).toEqual(mockPolitiques);
    expect(result.current.defaultRequirements).toEqual(mockDefaultRequirements);
    expect(result.current.error).toBeNull();
  });

  it('should handle errors during fetching', async () => {
    const errorMessage = 'Failed to load configuration';
    vi.mocked(planningService.fetchAllAgents).mockRejectedValueOnce(new Error(errorMessage));
    vi.mocked(planningService.fetchAllPolitiques).mockResolvedValueOnce(mockPolitiques);
    vi.mocked(planningService.fetchDefaultRequirements).mockResolvedValueOnce(mockDefaultRequirements);

    const { result } = renderHook(() => useConfiguration());

    await waitFor(() => expect(result.current.isLoading).toBe(false));

    expect(result.current.error).toBe(errorMessage);
    expect(result.current.agents).toEqual([]);
  });
});
