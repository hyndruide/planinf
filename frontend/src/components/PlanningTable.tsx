import React from 'react';
import type { AgentPlanning } from '../types/planning';

interface PlanningTableProps {
  agents: AgentPlanning[];
}

export const PlanningTable: React.FC<PlanningTableProps> = ({ agents }) => {
  if (!agents || agents.length === 0) {
    return <div style={{ padding: '20px', textAlign: 'center' }}>Aucun agent à afficher</div>;
  }

  // Get all unique dates from the first agent's planning to use as headers
  const dates = agents[0].planning.map(p => p.date);

  return (
    <div className="planning-table-container" style={{ overflowX: 'auto', border: '1px solid #e2e8f0', borderRadius: '8px' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', backgroundColor: 'white' }}>
        <thead style={{ backgroundColor: '#f8fafc' }}>
          <tr>
            <th style={{ padding: '12px', textAlign: 'left', borderBottom: '2px solid #e2e8f0', minWidth: '150px' }}>Agent</th>
            {dates.map(date => (
              <th key={date} style={{ padding: '12px', textAlign: 'center', borderBottom: '2px solid #e2e8f0', minWidth: '100px', fontSize: '0.85em' }}>
                {date}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {agents.map(agent => (
            <tr key={agent.agent_id} style={{ borderBottom: '1px solid #e2e8f0' }}>
              <td style={{ padding: '12px', fontWeight: 'bold' }}>{agent.nom}</td>
              {agent.planning.map((day, index) => {
                const isWork = day.shift.type === 'WORK';
                return (
                  <td 
                    key={`${agent.agent_id}-${day.date}-${index}`} 
                    style={{ 
                      padding: '12px', 
                      textAlign: 'center',
                      backgroundColor: isWork ? '#eff6ff' : '#f1f5f9',
                      color: isWork ? '#1e40af' : '#64748b'
                    }}
                  >
                    <div style={{ 
                      fontSize: '0.75em', 
                      fontWeight: 'bold',
                      padding: '4px',
                      borderRadius: '4px',
                      border: isWork ? '1px solid #bfdbfe' : '1px solid #cbd5e1'
                    }}>
                      {day.shift.type}
                      {isWork && day.shift.duration > 0 && (
                        <span style={{ display: 'block', fontSize: '0.9em', fontWeight: 'normal' }}>
                          ({day.shift.duration}h)
                        </span>
                      )}
                    </div>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
