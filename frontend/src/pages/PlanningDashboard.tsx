import React, { useEffect, useState } from 'react';
import { usePlanning } from '../hooks/usePlanning';
import { PlanningTable } from '../components/PlanningTable';
import { GeneratePlanningForm } from '../components/GeneratePlanningForm';

export const PlanningDashboard: React.FC = () => {
  // We use fixed params for now as per the mock strategy
  const { planningData, coverageData, isLoading, isGenerating, error, triggerFetch, generateSchedule } = usePlanning('2026-01-01', 2);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    triggerFetch();
  }, [triggerFetch]);

  if (isLoading && !isGenerating) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <div className="spinner"></div>
        <p>Chargement du planning...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container" style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <header style={{ marginBottom: '30px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '2px solid #3b82f6', paddingBottom: '10px' }}>
        <h1 style={{ color: '#0f172a', margin: 0 }}>
          Tableau de Bord de Planification
        </h1>
        <button 
          onClick={() => setShowForm(!showForm)}
          style={{ 
            backgroundColor: showForm ? '#e2e8f0' : '#3b82f6', 
            color: showForm ? '#1e293b' : 'white',
            padding: '8px 16px',
            borderRadius: '6px',
            border: 'none',
            fontWeight: 'bold',
            cursor: 'pointer'
          }}
        >
          {showForm ? 'Masquer le générateur' : 'Générer un planning'}
        </button>
      </header>

      {error && (
        <div style={{ padding: '20px', color: '#991b1b', backgroundColor: '#fee2e2', borderRadius: '8px', margin: '20px 0' }}>
          <strong>Erreur :</strong> {error}
        </div>
      )}

      {showForm && (
        <GeneratePlanningForm 
          onSubmit={async (payload) => {
            await generateSchedule(payload);
            setShowForm(false);
          }} 
          isGenerating={isGenerating} 
        />
      )}

      <section>
        <h3 style={{ marginBottom: '15px' }}>Grille des Affectations</h3>
        <PlanningTable agents={planningData} coverageData={coverageData} />
      </section>
    </div>
  );
};
