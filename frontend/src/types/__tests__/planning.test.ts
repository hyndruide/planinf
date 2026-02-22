import { describe, it, expect } from 'vitest';
import type { ShiftType, AgentPlanning, DayCoverage, GeneratePlanningPayload, GeneratePlanningResponse, Agent, Politique } from '../planning';

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

  it('should allow creating a valid GeneratePlanningPayload object', () => {
    const payload: GeneratePlanningPayload = {
      agent_ids: ['uuid-1', 'uuid-2'],
      politique_ids: ['pol-uuid-1', 'pol-uuid-2'],
      duree_cycle: 84,
      date_debut: '2026-01-01'
    };

    expect(payload.duree_cycle).toBe(84);
    expect(payload.agent_ids.length).toBe(2);
    expect(payload.politique_ids.length).toBe(2);
  });

  it('should allow creating a valid Agent type', () => {
    const agent: Agent = {
      id: 'agent-1',
      nom: 'Alice',
      quotite: 1.0
    };
    expect(agent.nom).toBe('Alice');
  });

  it('should allow creating a valid Politique type', () => {
    const politique: Politique = {
      id: 'pol-1',
      nom: 'Code du travail'
    };
    expect(politique.nom).toBe('Code du travail');
  });

  it('should allow creating a valid GeneratePlanningResponse object', () => {
    const response: GeneratePlanningResponse = {
      message: 'Schedule generated successfully'
    };

    expect(response.message).toBe('Schedule generated successfully');
  });
});
