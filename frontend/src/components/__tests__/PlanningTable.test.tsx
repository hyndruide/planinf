import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { PlanningTable } from '../PlanningTable';
import type { AgentPlanning } from '../../types/planning';

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

  it('should render agent names', () => {
    render(<PlanningTable agents={mockPlanning} />);
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('Bob')).toBeInTheDocument();
  });

  it('should render dates in the header', () => {
    render(<PlanningTable agents={mockPlanning} />);
    expect(screen.getByText('2026-01-01')).toBeInTheDocument();
    expect(screen.getByText('2026-01-02')).toBeInTheDocument();
  });

  it('should render shift cells with correct content', () => {
    render(<PlanningTable agents={mockPlanning} />);
    
    // Check Alice's cells
    const aliceRow = screen.getByText('Alice').closest('tr');
    expect(aliceRow).toContainElement(screen.getAllByText('WORK')[0]);
    expect(aliceRow).toContainElement(screen.getAllByText('REST')[0]);

    // Check Bob's cells
    const bobRow = screen.getByText('Bob').closest('tr');
    expect(bobRow).toContainElement(screen.getAllByText('REST')[1]);
    expect(bobRow).toContainElement(screen.getAllByText('WORK')[1]);
  });

  it('should render an empty state if no agents are provided', () => {
    render(<PlanningTable agents={[]} />);
    expect(screen.getByText(/Aucun agent à afficher/i)).toBeInTheDocument();
  });
});
