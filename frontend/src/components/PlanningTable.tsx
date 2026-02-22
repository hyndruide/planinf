import React from 'react';
import type { AgentPlanning, DayCoverage } from '../types/planning';
import { format, parseISO } from 'date-fns';
import { fr } from 'date-fns/locale';
import { Briefcase, Coffee } from 'lucide-react';

interface PlanningTableProps {
  agents: AgentPlanning[];
  coverageData: DayCoverage[];
}

export const PlanningTable: React.FC<PlanningTableProps> = ({ agents, coverageData }) => {
  if (!agents || agents.length === 0) {
    return <div style={{ padding: '20px', textAlign: 'center', color: '#1e293b' }}>Aucun agent à afficher</div>;
  }

  // Get all unique dates from the first agent's planning to use as headers
  const dates = agents[0].planning.map(p => p.date);

  return (
    <div className="planning-table-container" style={{ overflowX: 'auto', border: '1px solid #e2e8f0', borderRadius: '8px' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', backgroundColor: 'white', color: '#1e293b', minWidth: '800px' }}>
        <thead style={{ backgroundColor: '#f8fafc' }}>
          <tr>
            <th style={{ 
              padding: '12px', 
              textAlign: 'left', 
              borderBottom: '2px solid #e2e8f0', 
              minWidth: '150px', 
              color: '#334155',
              position: 'sticky',
              left: 0,
              backgroundColor: '#f8fafc',
              zIndex: 10,
              borderRight: '1px solid #e2e8f0'
            }}>
              Agent
            </th>
            {dates.map(dateStr => {
              const date = parseISO(dateStr);
              return (
                <th key={dateStr} style={{ 
                  padding: '8px', 
                  textAlign: 'center', 
                  borderBottom: '2px solid #e2e8f0', 
                  minWidth: '60px', 
                  fontSize: '0.85em', 
                  color: '#334155' 
                }}>
                  <div style={{ fontWeight: 'normal', fontSize: '0.9em', color: '#64748b', textTransform: 'capitalize' }}>
                    {format(date, 'E', { locale: fr })}
                  </div>
                  <div style={{ fontWeight: 'bold' }}>
                    {format(date, 'dd/MM', { locale: fr })}
                  </div>
                </th>
              );
            })}
          </tr>
        </thead>
        <tbody>
          {agents.map(agent => (
            <tr key={agent.agent_id} style={{ borderBottom: '1px solid #e2e8f0' }}>
              <td style={{ 
                padding: '12px', 
                fontWeight: 'bold',
                position: 'sticky',
                left: 0,
                backgroundColor: 'white',
                zIndex: 10,
                borderRight: '1px solid #e2e8f0'
              }}>
                {agent.nom}
              </td>
              {agent.planning.map((day, index) => {
                const isWork = day.shift.type === 'WORK';
                return (
                  <td 
                    key={`${agent.agent_id}-${day.date}-${index}`} 
                    style={{ 
                      padding: '8px', 
                      textAlign: 'center',
                      backgroundColor: isWork ? '#eff6ff' : '#f8fafc',
                      color: isWork ? '#1e40af' : '#64748b'
                    }}
                  >
                    <div style={{ 
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      padding: '4px',
                      borderRadius: '4px',
                      border: isWork ? '1px solid #bfdbfe' : '1px dashed #cbd5e1',
                      height: '48px'
                    }}>
                      {isWork ? (
                        <Briefcase size={16} data-testid="icon-work" />
                      ) : (
                        <Coffee size={16} data-testid="icon-rest" opacity={0.5} />
                      )}
                      
                      {isWork && day.shift.duration > 0 && (
                        <span style={{ fontSize: '0.75em', marginTop: '2px' }}>
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
        <tfoot style={{ backgroundColor: '#f8fafc', fontWeight: 'bold', borderTop: '2px solid #cbd5e1' }}>
          <tr>
            <td style={{ 
              padding: '12px', 
              textAlign: 'left', 
              color: '#334155',
              position: 'sticky',
              left: 0,
              backgroundColor: '#f8fafc',
              zIndex: 10,
              borderRight: '1px solid #e2e8f0'
            }}>
              Couverture (Gap)
            </td>
            {dates.map(date => {
              const coverage = coverageData.find(c => c.date === date);
              if (!coverage) return <td key={`cov-${date}`}>-</td>;
              
              let bgColor = '#dcfce7'; // green for ok
              let textColor = '#166534';
              let text = 'OK';
              
              if (coverage.gap > 0) {
                bgColor = '#dbeafe'; // blue for surplus
                textColor = '#1e40af';
                text = `+${coverage.gap}`;
              } else if (coverage.gap < 0) {
                bgColor = '#fee2e2'; // red for deficit
                textColor = '#991b1b';
                text = `${coverage.gap}`;
              }
              
              return (
                <td key={`cov-${date}`} style={{ padding: '8px', textAlign: 'center' }}>
                  <div style={{
                    backgroundColor: bgColor,
                    color: textColor,
                    padding: '4px',
                    borderRadius: '4px',
                    fontSize: '0.8em',
                    border: `1px solid ${textColor}40`,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    <span>{text}</span>
                    <span style={{ fontSize: '0.8em', fontWeight: 'normal', opacity: 0.8 }}>
                      ({coverage.present_count}/{coverage.required_count})
                    </span>
                  </div>
                </td>
              );
            })}
          </tr>
        </tfoot>
      </table>
    </div>
  );
};
