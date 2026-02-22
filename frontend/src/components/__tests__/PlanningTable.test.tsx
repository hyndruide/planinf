import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { PlanningTable } from '../PlanningTable';
import type { AgentPlanning, DayCoverage } from '../../types/planning';

describe('PlanningTable Component', () => {
  const mockPlanning: AgentPlanning[] = [
    {
      agent_id: '1',
      nom: 'Alice',
      planning: [
        { date: '2026-01-01', shift: { type: 'WORK', duration: 12 } },
        { date: '2026-01-02', shift: { type: 'REST', duration: 0 } }
      ]
    },
    {
      agent_id: '2',
      nom: 'Bob',
      planning: [
        { date: '2026-01-01', shift: { type: 'REST', duration: 0 } },
        { date: '2026-01-02', shift: { type: 'WORK', duration: 12 } }
      ]
    }
  ];

  const mockCoverage: DayCoverage[] = [
    { date: '2026-01-01', present_count: 1, required_count: 2, gap: -1 },
    { date: '2026-01-02', present_count: 1, required_count: 1, gap: 0 }
  ];

  it('should render agent names', () => {
    render(<PlanningTable agents={mockPlanning} coverageData={mockCoverage} />);
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('Bob')).toBeInTheDocument();
  });

  it('should render dual-row dates in the header in French', () => {
    render(<PlanningTable agents={mockPlanning} coverageData={mockCoverage} />);
    // 2026-01-01 is a Thursday (jeudi)
    expect(screen.getByText('01/01')).toBeInTheDocument();
    expect(screen.getByText('jeu.')).toBeInTheDocument();
    
    // 2026-01-02 is a Friday (vendredi)
    expect(screen.getByText('02/01')).toBeInTheDocument();
    expect(screen.getByText('ven.')).toBeInTheDocument();
  });

  it('should render shift cells with icons and duration', () => {
    render(<PlanningTable agents={mockPlanning} coverageData={mockCoverage} />);
    
    const aliceRow = screen.getByText('Alice').closest('tr');
    
    // Check for icons using data-testid
    expect(aliceRow?.querySelector('[data-testid="icon-work"]')).toBeInTheDocument();
    expect(aliceRow?.querySelector('[data-testid="icon-rest"]')).toBeInTheDocument();
    
    // Duration is rendered for WORK
    expect(aliceRow).toContainElement(screen.getAllByText('(12h)')[0]);
  });

  it('should render coverage data in footer', () => {
    render(<PlanningTable agents={mockPlanning} coverageData={mockCoverage} />);
    expect(screen.getByText('Couverture (Gap)')).toBeInTheDocument();
    expect(screen.getByText('-1')).toBeInTheDocument(); // gap: -1
    expect(screen.getByText('OK')).toBeInTheDocument(); // gap: 0
  });

  it('should render an empty state if no agents are provided', () => {
    render(<PlanningTable agents={[]} coverageData={[]} />);
    expect(screen.getByText(/Aucun agent à afficher/i)).toBeInTheDocument();
  });
});
