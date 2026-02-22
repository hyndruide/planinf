import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CoverageSummary } from '../CoverageSummary';
import { DayCoverage } from '../../types/planning';

describe('CoverageSummary Component', () => {
  it('should render a list of coverage items', () => {
    const mockData: DayCoverage[] = [
      { date: '2026-01-01', present_count: 2, required_count: 2, gap: 0 },
      { date: '2026-01-02', present_count: 3, required_count: 2, gap: 1 },
      { date: '2026-01-03', present_count: 1, required_count: 2, gap: -1 }
    ];

    render(<CoverageSummary coverageData={mockData} />);

    // Check if dates are rendered
    expect(screen.getByText('2026-01-01')).toBeInTheDocument();
    expect(screen.getByText('2026-01-02')).toBeInTheDocument();
    expect(screen.getByText('2026-01-03')).toBeInTheDocument();

    // Check if the gap labels are rendered correctly based on gap
    expect(screen.getByText(/Atteint/i)).toBeInTheDocument(); // For gap 0
    expect(screen.getByText(/Surplus:\s*\+?1/i)).toBeInTheDocument(); // For gap 1
    expect(screen.getByText(/Déficit:\s*-1/i)).toBeInTheDocument(); // For gap -1
  });

  it('should render a fallback message if no data is provided', () => {
    render(<CoverageSummary coverageData={[]} />);
    expect(screen.getByText(/Aucune donnée de couverture/i)).toBeInTheDocument();
  });
});
