import { useState, useCallback } from 'react';
import type { AgentPlanning, DayCoverage, GeneratePlanningPayload, GeneratePlanningResponse } from '../types/planning';
import { fetchFullPlanning, fetchCoverageAnalysis, generatePlanning } from '../services/planningService';

interface UsePlanningResult {
  planningData: AgentPlanning[];
  coverageData: DayCoverage[];
  isLoading: boolean;
  isGenerating: boolean;
  error: string | null;
  triggerFetch: () => void;
  generateSchedule: (payload: GeneratePlanningPayload) => Promise<GeneratePlanningResponse | void>;
}

export const usePlanning = (startDate: string, weeks: number = 12): UsePlanningResult => {
  const [planningData, setPlanningData] = useState<AgentPlanning[]>([]);
  const [coverageData, setCoverageData] = useState<DayCoverage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
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

  const generateSchedule = useCallback(async (payload: GeneratePlanningPayload) => {
    setIsGenerating(true);
    setError(null);
    try {
      const response = await generatePlanning(payload);
      // Fetch new data after successful generation
      await triggerFetch();
      return response;
    } catch (err) {
      if (err instanceof Error) {
        setError(`Erreur de génération : ${err.message}`);
      } else {
        setError('Erreur de génération inconnue');
      }
    } finally {
      setIsGenerating(false);
    }
  }, [triggerFetch]);

  return {
    planningData,
    coverageData,
    isLoading,
    isGenerating,
    error,
    triggerFetch,
    generateSchedule
  };
};
