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

  it('should render dates in the header', () => {
    render(<PlanningTable agents={mockPlanning} coverageData={mockCoverage} />);
    expect(screen.getByText('2026-01-01')).toBeInTheDocument();
    expect(screen.getByText('2026-01-02')).toBeInTheDocument();
  });

  it('should render shift cells with correct content', () => {
    render(<PlanningTable agents={mockPlanning} coverageData={mockCoverage} />);
    
    const aliceRow = screen.getByText('Alice').closest('tr');
    expect(aliceRow).toContainElement(screen.getAllByText('WORK')[0]);
    expect(aliceRow).toContainElement(screen.getAllByText('REST')[0]);
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
