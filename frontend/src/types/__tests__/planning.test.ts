import { describe, it, expect } from 'vitest';
import type { ShiftType, AgentPlanning, DayCoverage } from '../planning';

describe('Planning Domain Types', () => {
  it('should have valid ShiftType values', () => {
    const work: ShiftType = 'WORK';
    const rest: ShiftType = 'REST';
    expect(work).toBe('WORK');
    expect(rest).toBe('REST');
  });

  it('should allow creating a valid AgentPlanning object', () => {
    const mockAgent: AgentPlanning = {
      agent_id: 'uuid-1',
      nom: 'Alice',
      planning: [
        {
          date: '2026-01-01',
          shift: {
            type: 'WORK',
            duration: 12
          }
        }
      ]
    };

    expect(mockAgent.nom).toBe('Alice');
    expect(mockAgent.planning[0].shift.type).toBe('WORK');
  });

  it('should allow creating a valid DayCoverage object', () => {
    const mockCoverage: DayCoverage = {
      date: '2026-01-01',
      present_count: 2,
      required_count: 2,
      gap: 0
    };

    expect(mockCoverage.gap).toBe(0);
  });
});
