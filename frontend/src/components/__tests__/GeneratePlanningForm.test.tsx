import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { GeneratePlanningForm } from '../GeneratePlanningForm';
import * as configurationHook from '../../hooks/useConfiguration';
import { mockAgents, mockPolitiques, mockDefaultRequirements } from '../../mocks/planningData';

// Mock the hook
vi.mock('../../hooks/useConfiguration');

describe('GeneratePlanningForm Component', () => {
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    vi.stubGlobal('alert', vi.fn());
    
    // Default mock implementation
    vi.mocked(configurationHook.useConfiguration).mockReturnValue({
      agents: mockAgents,
      politiques: mockPolitiques,
      defaultRequirements: mockDefaultRequirements,
      isLoading: false,
      error: null
    });
  });

  it('should render all form fields including agent checkboxes and requirement grid', () => {
    render(<GeneratePlanningForm onSubmit={mockOnSubmit} isGenerating={false} />);
    
    expect(screen.getByLabelText(/Date de début/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Durée du cycle/i)).toBeInTheDocument();
    expect(screen.getByText(/Sélection des Politiques/i)).toBeInTheDocument();
    expect(screen.getByText(/Sélection des Agents/i)).toBeInTheDocument();
    expect(screen.getByText(/Saisie du besoin/i)).toBeInTheDocument();
    
    // Check if daily requirements inputs are rendered
    mockDefaultRequirements.forEach(req => {
      expect(screen.getByLabelText(req.day)).toBeInTheDocument();
    });
    
    // Check if mock agents are rendered as checkboxes
    mockAgents.forEach(agent => {
      expect(screen.getByLabelText(agent.nom, { exact: false })).toBeInTheDocument();
    });
  });

  it('should submit the form with selected agents, policies and requirements', async () => {
    const user = userEvent.setup();
    render(<GeneratePlanningForm onSubmit={mockOnSubmit} isGenerating={false} />);
    
    // Change a requirement
    const mondayInput = screen.getByLabelText(/Lundi/i);
    await user.clear(mondayInput);
    await user.type(mondayInput, '5');

    // Submit
    const submitButton = screen.getByRole('button', { name: /Générer/i });
    await user.click(submitButton);
    
    expect(mockOnSubmit).toHaveBeenCalledTimes(1);
    const call = mockOnSubmit.mock.calls[0][0];
    
    expect(call.daily_requirements).toBeDefined();
    const mondayReq = call.daily_requirements.find((r: any) => r.day === 'Lundi');
    expect(mondayReq.count).toBe(5);
  });

  it('should submit the form with selected agents and policies', async () => {
    const user = userEvent.setup();
    render(<GeneratePlanningForm onSubmit={mockOnSubmit} isGenerating={false} />);
    
    // By default all agents are selected. Let's deselect some.
    const agent1 = screen.getByLabelText(mockAgents[0].nom, { exact: false });
    const agent2 = screen.getByLabelText(mockAgents[1].nom, { exact: false });
    await user.click(agent1); // Deselect uuid-1
    await user.click(agent2); // Deselect uuid-2

    // By default first policy is selected.
    const pol2 = screen.getByLabelText(mockPolitiques[1].nom, { exact: false });
    await user.click(pol2); // Add uuid-pol-2
    
    // Submit
    const submitButton = screen.getByRole('button', { name: /Générer/i });
    await user.click(submitButton);
    
    expect(mockOnSubmit).toHaveBeenCalledTimes(1);
    const call = mockOnSubmit.mock.calls[0][0];
    // uuid-1 and uuid-2 should NOT be there because they were deselected
    expect(call.agent_ids).not.toContain(mockAgents[0].id);
    expect(call.agent_ids).not.toContain(mockAgents[1].id);
    // uuid-3, 4, 5 should still be there (default)
    expect(call.agent_ids).toContain(mockAgents[2].id);
    
    expect(call.politique_ids).toContain(mockPolitiques[0].id); // default
    expect(call.politique_ids).toContain(mockPolitiques[1].id); // added
  });

  it('should show loading state when configuration is loading', () => {
    vi.mocked(configurationHook.useConfiguration).mockReturnValue({
      agents: [],
      politiques: [],
      defaultRequirements: [],
      isLoading: true,
      error: null
    });

    render(<GeneratePlanningForm onSubmit={mockOnSubmit} isGenerating={false} />);
    expect(screen.getByText(/Chargement de la configuration/i)).toBeInTheDocument();
  });

  it('should show error state when configuration fails', () => {
    vi.mocked(configurationHook.useConfiguration).mockReturnValue({
      agents: [],
      politiques: [],
      defaultRequirements: [],
      isLoading: false,
      error: 'Erreur de chargement'
    });

    render(<GeneratePlanningForm onSubmit={mockOnSubmit} isGenerating={false} />);
    expect(screen.getByText(/Erreur : Erreur de chargement/i)).toBeInTheDocument();
  });

  it('should disable form elements when isGenerating is true', () => {
    render(<GeneratePlanningForm onSubmit={mockOnSubmit} isGenerating={true} />);
    
    expect(screen.getByLabelText(/Date de début/i)).toBeDisabled();
    expect(screen.getByLabelText(/Durée du cycle/i)).toBeDisabled();
    
    // All agent checkboxes should be disabled
    mockAgents.forEach(agent => {
      expect(screen.getByLabelText(agent.nom, { exact: false })).toBeDisabled();
    });
    
    expect(screen.getByRole('button', { name: /Génération en cours/i })).toBeDisabled();
  });
});
