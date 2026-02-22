import React, { useEffect } from 'react';
import { usePlanning } from '../hooks/usePlanning';
import { PlanningTable } from '../components/PlanningTable';

export const PlanningDashboard: React.FC = () => {
  // We use fixed params for now as per the mock strategy
  const { planningData, coverageData, isLoading, error, triggerFetch } = usePlanning('2026-01-01', 2);

  useEffect(() => {
    triggerFetch();
  }, [triggerFetch]);

  if (isLoading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <div className="spinner"></div>
        <p>Chargement du planning...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '20px', color: '#991b1b', backgroundColor: '#fee2e2', borderRadius: '8px', margin: '20px' }}>
        <strong>Erreur :</strong> {error}
      </div>
    );
  }

  return (
    <div className="dashboard-container" style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <header style={{ marginBottom: '30px' }}>
        <h1 style={{ color: '#0f172a', borderBottom: '2px solid #3b82f6', paddingBottom: '10px' }}>
          Tableau de Bord de Planification
        </h1>
      </header>

      <section>
        <h3 style={{ marginBottom: '15px' }}>Grille des Affectations</h3>
        <PlanningTable agents={planningData} coverageData={coverageData} />
      </section>
    </div>
  );
};
