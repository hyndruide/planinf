import { describe, it, expect } from 'vitest';
import { mockAgentPlanning, mockDayCoverage } from '../planningData';
import { AgentPlanning, DayCoverage } from '../../types/planning';

describe('Planning Mock Data', () => {
  it('should have mockAgentPlanning exported as an array', () => {
    expect(Array.isArray(mockAgentPlanning)).toBe(true);
    expect(mockAgentPlanning.length).toBeGreaterThan(0);
  });

  it('should contain valid AgentPlanning objects with 14-21 days of planning', () => {
    const agent: AgentPlanning = mockAgentPlanning[0];
    
    expect(agent).toHaveProperty('agent_id');
    expect(agent).toHaveProperty('nom');
    expect(Array.isArray(agent.planning)).toBe(true);
    
    // We expect 14 to 21 days
    expect(agent.planning.length).toBeGreaterThanOrEqual(14);
    expect(agent.planning.length).toBeLessThanOrEqual(21);
    
    // Check structure of a planned day
    const firstDay = agent.planning[0];
    expect(firstDay).toHaveProperty('date');
    expect(firstDay).toHaveProperty('shift');
    expect(['WORK', 'REST']).toContain(firstDay.shift.type);
    expect(typeof firstDay.shift.duration).toBe('number');
  });

  it('should have mockDayCoverage exported as an array', () => {
    expect(Array.isArray(mockDayCoverage)).toBe(true);
    expect(mockDayCoverage.length).toBeGreaterThan(0);
  });

  it('should contain valid DayCoverage objects', () => {
    const coverage: DayCoverage = mockDayCoverage[0];
    
    expect(coverage).toHaveProperty('date');
    expect(coverage).toHaveProperty('present_count');
    expect(coverage).toHaveProperty('required_count');
    expect(coverage).toHaveProperty('gap');
    
    // gap should be present_count - required_count
    expect(coverage.gap).toBe(coverage.present_count - coverage.required_count);
  });
});
