import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { GeneratePlanningForm } from '../GeneratePlanningForm';

describe('GeneratePlanningForm Component', () => {
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    // Prevent alert from crashing tests
    vi.stubGlobal('alert', vi.fn());
  });

  it('should render all form fields', () => {
    render(<GeneratePlanningForm onSubmit={mockOnSubmit} isGenerating={false} />);
    
    expect(screen.getByLabelText(/Date de début/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Durée du cycle/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Politique de conformité/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Agents/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Générer \(Solveur\)/i })).toBeInTheDocument();
  });

  it('should submit the form with correctly formatted payload', async () => {
    const user = userEvent.setup();
    render(<GeneratePlanningForm onSubmit={mockOnSubmit} isGenerating={false} />);
    
    // Clear and type into agent ids
    const agentInput = screen.getByLabelText(/Agents/i);
    await user.clear(agentInput);
    await user.type(agentInput, 'agent-1, agent-2 , agent-3');
    
    // Submit
    const submitButton = screen.getByRole('button', { name: /Générer/i });
    await user.click(submitButton);
    
    expect(mockOnSubmit).toHaveBeenCalledTimes(1);
    expect(mockOnSubmit).toHaveBeenCalledWith({
      date_debut: '2026-01-01',
      duree_cycle: 84,
      politique_id: 'pol-1',
      agent_ids: ['agent-1', 'agent-2', 'agent-3']
    });
  });

  it('should prevent submission if fields are empty', async () => {
    const user = userEvent.setup();
    render(<GeneratePlanningForm onSubmit={mockOnSubmit} isGenerating={false} />);
    
    // Clear agent input to trigger validation
    const agentInput = screen.getByLabelText(/Agents/i);
    await user.clear(agentInput);
    
    const submitButton = screen.getByRole('button', { name: /Générer/i });
    await user.click(submitButton);
    
    expect(mockOnSubmit).not.toHaveBeenCalled();
    expect(window.alert).toHaveBeenCalledWith('Veuillez remplir tous les champs');
  });

  it('should disable form elements when isGenerating is true', () => {
    render(<GeneratePlanningForm onSubmit={mockOnSubmit} isGenerating={true} />);
    
    expect(screen.getByLabelText(/Date de début/i)).toBeDisabled();
    expect(screen.getByLabelText(/Durée du cycle/i)).toBeDisabled();
    expect(screen.getByLabelText(/Politique de conformité/i)).toBeDisabled();
    expect(screen.getByLabelText(/Agents/i)).toBeDisabled();
    expect(screen.getByRole('button', { name: /Génération en cours/i })).toBeDisabled();
  });
});
