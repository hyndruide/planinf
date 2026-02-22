import { useState, useEffect } from 'react';
import type { Agent, Politique, DailyRequirementInput } from '../types/planning';
import { fetchAllAgents, fetchAllPolitiques, fetchDefaultRequirements } from '../services/planningService';

interface UseConfigurationResult {
  agents: Agent[];
  politiques: Politique[];
  defaultRequirements: DailyRequirementInput[];
  isLoading: boolean;
  error: string | null;
}

export const useConfiguration = (): UseConfigurationResult => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [politiques, setPolitiques] = useState<Politique[]>([]);
  const [defaultRequirements, setDefaultRequirements] = useState<DailyRequirementInput[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadConfig = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const [loadedAgents, loadedPolitiques, loadedRequirements] = await Promise.all([
          fetchAllAgents(),
          fetchAllPolitiques(),
          fetchDefaultRequirements()
        ]);
        
        setAgents(loadedAgents);
        setPolitiques(loadedPolitiques);
        setDefaultRequirements(loadedRequirements);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError('Failed to load configuration options');
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadConfig();
  }, []);

  return {
    agents,
    politiques,
    defaultRequirements,
    isLoading,
    error
  };
};
