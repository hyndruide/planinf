import React from 'react';
import { DayCoverage } from '../types/planning';

interface CoverageSummaryProps {
  coverageData: DayCoverage[];
}

export const CoverageSummary: React.FC<CoverageSummaryProps> = ({ coverageData }) => {
  if (!coverageData || coverageData.length === 0) {
    return <div>Aucune donnée de couverture</div>;
  }

  return (
    <div className="coverage-summary" style={{ margin: '20px 0' }}>
      <h3>Couverture Quotidienne</h3>
      <div className="coverage-grid" style={{ display: 'flex', gap: '10px', overflowX: 'auto', paddingBottom: '10px' }}>
        {coverageData.map((day) => {
          let statusText = 'Atteint';
          let bgColor = '#dcfce7'; // light green
          let color = '#166534';

          if (day.gap > 0) {
            statusText = `Surplus: +${day.gap}`;
            bgColor = '#dbeafe'; // light blue
            color = '#1e40af';
          } else if (day.gap < 0) {
            statusText = `Déficit: ${day.gap}`;
            bgColor = '#fee2e2'; // light red
            color = '#991b1b';
          }

          return (
            <div 
              key={day.date} 
              className="coverage-day" 
              style={{ 
                border: `1px solid ${color}`, 
                padding: '10px', 
                borderRadius: '6px',
                minWidth: '120px',
                textAlign: 'center',
                backgroundColor: bgColor,
                color: color
              }}
            >
              <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>{day.date}</div>
              <div style={{ fontSize: '0.9em' }}>
                Présents: {day.present_count}<br/>
                Requis: {day.required_count}
              </div>
              <div style={{ marginTop: '8px', fontWeight: 'bold' }}>{statusText}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
