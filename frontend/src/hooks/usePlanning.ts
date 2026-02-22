import { useState, useCallback } from 'react';
import type { AgentPlanning, DayCoverage } from '../types/planning';
import { fetchFullPlanning, fetchCoverageAnalysis } from '../services/planningService';

interface UsePlanningResult {
  planningData: AgentPlanning[];
  coverageData: DayCoverage[];
  isLoading: boolean;
  error: string | null;
  triggerFetch: () => void;
}

export const usePlanning = (startDate: string, weeks: number = 12): UsePlanningResult => {
  const [planningData, setPlanningData] = useState<AgentPlanning[]>([]);
  const [coverageData, setCoverageData] = useState<DayCoverage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const triggerFetch = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const planningPromise = fetchFullPlanning(startDate, weeks);
      
      // Calculate end date based on weeks
      const endDateObj = new Date(startDate);
      endDateObj.setDate(endDateObj.getDate() + (weeks * 7) - 1);
      const endDate = endDateObj.toISOString().split('T')[0];
      
      const coveragePromise = fetchCoverageAnalysis(startDate, endDate);

      const [planning, coverage] = await Promise.all([planningPromise, coveragePromise]);
      
      setPlanningData(planning);
      setCoverageData(coverage);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
      setPlanningData([]);
      setCoverageData([]);
    } finally {
      setIsLoading(false);
    }
  }, [startDate, weeks]);

  return {
    planningData,
    coverageData,
    isLoading,
    error,
    triggerFetch
  };
};
