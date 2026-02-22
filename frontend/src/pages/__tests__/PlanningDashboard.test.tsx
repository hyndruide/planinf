import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { PlanningDashboard } from '../PlanningDashboard';
import { usePlanning } from '../../hooks/usePlanning';
import { mockAgentPlanning, mockDayCoverage, mockAgents, mockPolitiques, mockDefaultRequirements } from '../../mocks/planningData';
import { format, parseISO } from 'date-fns';
import { fr } from 'date-fns/locale';
import * as configurationHook from '../../hooks/useConfiguration';

// Mock the hooks
vi.mock('../../hooks/usePlanning');
vi.mock('../../hooks/useConfiguration');

describe('PlanningDashboard Page', () => {
  const mockTriggerFetch = vi.fn();
  const mockGenerateSchedule = vi.fn().mockResolvedValue({});

  beforeEach(() => {
    vi.clearAllMocks();
    
    vi.mocked(configurationHook.useConfiguration).mockReturnValue({
      agents: mockAgents,
      politiques: mockPolitiques,
      defaultRequirements: mockDefaultRequirements,
      isLoading: false,
      error: null
    });
  });

  it('should render loading state initially', () => {
    vi.mocked(usePlanning).mockReturnValue({
      planningData: [],
      coverageData: [],
      isLoading: true,
      isGenerating: false,
      error: null,
      triggerFetch: mockTriggerFetch,
      generateSchedule: mockGenerateSchedule
    });

    render(<PlanningDashboard />);
    expect(screen.getByText(/Chargement du planning/i)).toBeInTheDocument();
  });

  it('should render error message if hook returns error', () => {
    vi.mocked(usePlanning).mockReturnValue({
      planningData: [],
      coverageData: [],
      isLoading: false,
      isGenerating: false,
      error: 'Erreur API',
      triggerFetch: mockTriggerFetch,
      generateSchedule: mockGenerateSchedule
    });

    render(<PlanningDashboard />);
    expect(screen.getByText(/Erreur API/i)).toBeInTheDocument();
  });

  it('should render components when data is loaded', () => {
    vi.mocked(usePlanning).mockReturnValue({
      planningData: mockAgentPlanning,
      coverageData: mockDayCoverage,
      isLoading: false,
      isGenerating: false,
      error: null,
      triggerFetch: mockTriggerFetch,
      generateSchedule: mockGenerateSchedule
    });

    render(<PlanningDashboard />);

    // Check titles
    expect(screen.getByText(/Tableau de Bord de Planification/i)).toBeInTheDocument();
    
    // Check if table is rendered by looking for its content
    expect(screen.getByText('Alice')).toBeInTheDocument();
    
    // Check if dates are rendered (now in DD/MM format)
    const formattedDate = format(parseISO(mockDayCoverage[0].date), 'dd/MM', { locale: fr });
    expect(screen.getAllByText(formattedDate).length).toBeGreaterThanOrEqual(1);
  });

  it('should toggle GeneratePlanningForm visibility', async () => {
    const user = userEvent.setup();
    vi.mocked(usePlanning).mockReturnValue({
      planningData: mockAgentPlanning,
      coverageData: mockDayCoverage,
      isLoading: false,
      isGenerating: false,
      error: null,
      triggerFetch: mockTriggerFetch,
      generateSchedule: mockGenerateSchedule
    });

    render(<PlanningDashboard />);
    
    // Form is not visible initially
    expect(screen.queryByText(/Configuration du Planning/i)).not.toBeInTheDocument();
    
    // Click button to show form
    const toggleButton = screen.getByRole('button', { name: /Générer un planning/i });
    await user.click(toggleButton);
    
    expect(screen.getByText(/Configuration du Planning/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Masquer le générateur/i })).toBeInTheDocument();
    
    // Click to hide again
    await user.click(screen.getByRole('button', { name: /Masquer le générateur/i }));
    expect(screen.queryByText(/Configuration du Planning/i)).not.toBeInTheDocument();
  });

  it('should submit GeneratePlanningForm and call generateSchedule', async () => {
    const user = userEvent.setup();
    vi.mocked(usePlanning).mockReturnValue({
      planningData: mockAgentPlanning,
      coverageData: mockDayCoverage,
      isLoading: false,
      isGenerating: false,
      error: null,
      triggerFetch: mockTriggerFetch,
      generateSchedule: mockGenerateSchedule
    });

    render(<PlanningDashboard />);
    
    // Open form
    await user.click(screen.getByRole('button', { name: /Générer un planning/i }));
    
    // Submit form (it will use default pre-selections from mock data)
    await user.click(screen.getByRole('button', { name: /Générer \(Solveur\)/i }));
    
    expect(mockGenerateSchedule).toHaveBeenCalledTimes(1);
    expect(mockGenerateSchedule).toHaveBeenCalledWith({
      date_debut: '2026-01-01',
      duree_cycle: 84,
      politique_ids: [mockPolitiques[0].id],
      agent_ids: mockAgents.map(a => a.id),
      daily_requirements: mockDefaultRequirements
    });
  });

  it('should call triggerFetch on mount', () => {
    vi.mocked(usePlanning).mockReturnValue({
      planningData: [],
      coverageData: [],
      isLoading: false,
      isGenerating: false,
      error: null,
      triggerFetch: mockTriggerFetch,
      generateSchedule: mockGenerateSchedule
    });

    render(<PlanningDashboard />);
    expect(mockTriggerFetch).toHaveBeenCalledTimes(1);
  });
});
