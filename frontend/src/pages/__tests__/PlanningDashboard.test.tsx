import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { PlanningDashboard } from '../PlanningDashboard';
import { usePlanning } from '../../hooks/usePlanning';
import { mockAgentPlanning, mockDayCoverage } from '../../mocks/planningData';

// Mock the hook
vi.mock('../../hooks/usePlanning');

describe('PlanningDashboard Page', () => {
  const mockTriggerFetch = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render loading state initially', () => {
    vi.mocked(usePlanning).mockReturnValue({
      planningData: [],
      coverageData: [],
      isLoading: true,
      error: null,
      triggerFetch: mockTriggerFetch
    });

    render(<PlanningDashboard />);
    expect(screen.getByText(/Chargement du planning/i)).toBeInTheDocument();
  });

  it('should render error message if hook returns error', () => {
    vi.mocked(usePlanning).mockReturnValue({
      planningData: [],
      coverageData: [],
      isLoading: false,
      error: 'Erreur API',
      triggerFetch: mockTriggerFetch
    });

    render(<PlanningDashboard />);
    expect(screen.getByText(/Erreur API/i)).toBeInTheDocument();
  });

  it('should render components when data is loaded', () => {
    vi.mocked(usePlanning).mockReturnValue({
      planningData: mockAgentPlanning,
      coverageData: mockDayCoverage,
      isLoading: false,
      error: null,
      triggerFetch: mockTriggerFetch
    });

    render(<PlanningDashboard />);

    // Check titles
    expect(screen.getByText(/Tableau de Bord de Planification/i)).toBeInTheDocument();
    expect(screen.getByText(/Couverture Quotidienne/i)).toBeInTheDocument();
    
    // Check if sub-components are rendered by looking for their content
    expect(screen.getByText('Alice')).toBeInTheDocument();
    
    // Using getAllByText because dates appear in both CoverageSummary and PlanningTable
    expect(screen.getAllByText(mockDayCoverage[0].date).length).toBeGreaterThanOrEqual(1);
  });

  it('should call triggerFetch on mount', () => {
    vi.mocked(usePlanning).mockReturnValue({
      planningData: [],
      coverageData: [],
      isLoading: false,
      error: null,
      triggerFetch: mockTriggerFetch
    });

    render(<PlanningDashboard />);
    expect(mockTriggerFetch).toHaveBeenCalledTimes(1);
  });
});
