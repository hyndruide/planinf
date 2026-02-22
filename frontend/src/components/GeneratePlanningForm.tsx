import React, { useState, useEffect } from 'react';
import type { GeneratePlanningPayload, DailyRequirementInput } from '../types/planning';
import { useConfiguration } from '../hooks/useConfiguration';

interface GeneratePlanningFormProps {
  onSubmit: (payload: GeneratePlanningPayload) => void;
  isGenerating: boolean;
}

export const GeneratePlanningForm: React.FC<GeneratePlanningFormProps> = ({ onSubmit, isGenerating }) => {
  const { agents, politiques, defaultRequirements, isLoading, error } = useConfiguration();
  
  const [dateDebut, setDateDebut] = useState('2026-01-01');
  const [dureeCycle, setDureeCycle] = useState<number>(84);
  const [selectedAgentIds, setSelectedAgentIds] = useState<string[]>([]);
  const [selectedPolitiqueIds, setSelectedPolitiqueIds] = useState<string[]>([]);
  const [dailyRequirements, setDailyRequirements] = useState<DailyRequirementInput[]>([]);

  // Pre-select data when loaded
  useEffect(() => {
    if (agents.length > 0 && selectedAgentIds.length === 0) {
      setSelectedAgentIds(agents.map(a => a.id));
    }
    if (politiques.length > 0 && selectedPolitiqueIds.length === 0) {
      setSelectedPolitiqueIds([politiques[0].id]);
    }
    if (defaultRequirements.length > 0 && dailyRequirements.length === 0) {
      setDailyRequirements(defaultRequirements);
    }
  }, [agents, politiques, defaultRequirements, selectedAgentIds.length, selectedPolitiqueIds.length, dailyRequirements.length]);

  const handleAgentToggle = (id: string) => {
    setSelectedAgentIds(prev => 
      prev.includes(id) ? prev.filter(a => a !== id) : [...prev, id]
    );
  };

  const handlePolitiqueToggle = (id: string) => {
    setSelectedPolitiqueIds(prev => 
      prev.includes(id) ? prev.filter(p => p !== id) : [...prev, id]
    );
  };

  const handleRequirementChange = (day: string, count: number) => {
    setDailyRequirements(prev => 
      prev.map(req => req.day === day ? { ...req, count } : req)
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!dateDebut || !dureeCycle || selectedAgentIds.length === 0 || selectedPolitiqueIds.length === 0) {
      alert('Veuillez remplir tous les champs et sélectionner au moins un agent et une politique');
      return;
    }

    const payload: GeneratePlanningPayload = {
      date_debut: dateDebut,
      duree_cycle: dureeCycle,
      politique_ids: selectedPolitiqueIds,
      agent_ids: selectedAgentIds,
      daily_requirements: dailyRequirements
    };

    onSubmit(payload);
  };

  if (isLoading) return <div style={{ padding: '20px' }}>Chargement de la configuration...</div>;
  if (error) return <div style={{ padding: '20px', color: 'red' }}>Erreur : {error}</div>;

  return (
    <div style={{ backgroundColor: '#f8fafc', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0', marginBottom: '30px' }}>
      <h3 style={{ marginTop: 0, marginBottom: '20px', color: '#1e293b' }}>Configuration du Planning</h3>
      <form onSubmit={handleSubmit}>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '20px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
            <label htmlFor="dateDebut" style={{ fontSize: '0.9em', fontWeight: 'bold', color: '#475569' }}>Date de début</label>
            <input 
              type="date" 
              id="dateDebut"
              value={dateDebut} 
              onChange={(e) => setDateDebut(e.target.value)}
              disabled={isGenerating}
              style={{ padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1', backgroundColor: '#ffffff', color: '#1e293b', width: '100%', boxSizing: 'border-box' }}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
            <label htmlFor="dureeCycle" style={{ fontSize: '0.9em', fontWeight: 'bold', color: '#475569' }}>Durée du cycle (jours)</label>
            <input 
              type="number" 
              id="dureeCycle"
              value={dureeCycle} 
              onChange={(e) => setDureeCycle(Number(e.target.value))}
              min="1"
              disabled={isGenerating}
              style={{ padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1', backgroundColor: '#ffffff', color: '#1e293b', width: '100%', boxSizing: 'border-box' }}
            />
          </div>
        </div>

        {/* Daily Requirements Grid */}
        <div style={{ backgroundColor: 'white', padding: '15px', borderRadius: '6px', border: '1px solid #e2e8f0', marginBottom: '20px' }}>
          <h4 style={{ marginTop: 0, marginBottom: '15px', fontSize: '1rem', color: '#1e293b' }}>Saisie du besoin (Nombre d'agents requis par jour)</h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(60px, 1fr))', gap: '10px' }}>
            {dailyRequirements.map((req) => (
              <div key={req.day} style={{ display: 'flex', flexDirection: 'column', gap: '5px', textAlign: 'center' }}>
                <label htmlFor={`req-${req.day}`} style={{ fontSize: '0.8em', fontWeight: 'bold', color: '#64748b' }}>{req.day}</label>
                <input 
                  type="number" 
                  id={`req-${req.day}`}
                  value={req.count} 
                  onChange={(e) => handleRequirementChange(req.day, Number(e.target.value))}
                  min="0"
                  disabled={isGenerating}
                  style={{ padding: '5px', borderRadius: '4px', border: '1px solid #cbd5e1', textAlign: 'center', backgroundColor: '#ffffff', color: '#1e293b', width: '100%', boxSizing: 'border-box' }}
                />
              </div>
            ))}
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
          {/* Politiques Selection */}
          <div style={{ backgroundColor: 'white', padding: '15px', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
            <h4 style={{ marginTop: 0, marginBottom: '10px', fontSize: '1rem', color: '#1e293b' }}>Sélection des Politiques</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '150px', overflowY: 'auto' }}>
              {politiques.map(pol => (
                <label key={pol.id} style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '0.9em', color: '#1e293b' }}>
                  <input 
                    type="checkbox" 
                    checked={selectedPolitiqueIds.includes(pol.id)}
                    onChange={() => handlePolitiqueToggle(pol.id)}
                    disabled={isGenerating}
                  />
                  {pol.nom}
                </label>
              ))}
            </div>
          </div>

          {/* Agents Selection */}
          <div style={{ backgroundColor: 'white', padding: '15px', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
            <h4 style={{ marginTop: 0, marginBottom: '10px', fontSize: '1rem', color: '#1e293b' }}>Sélection des Agents</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '150px', overflowY: 'auto' }}>
              {agents.map(agent => (
                <label key={agent.id} style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '0.9em', color: '#1e293b' }}>
                  <input 
                    type="checkbox" 
                    checked={selectedAgentIds.includes(agent.id)}
                    onChange={() => handleAgentToggle(agent.id)}
                    disabled={isGenerating}
                  />
                  {agent.nom} <span style={{ color: '#64748b', fontSize: '0.85em' }}>({agent.quotite * 100}%)</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button 
            type="submit" 
            disabled={isGenerating}
            style={{ 
              backgroundColor: isGenerating ? '#94a3b8' : '#2563eb', 
              color: 'white', 
              padding: '12px 24px', 
              borderRadius: '6px', 
              border: 'none',
              cursor: isGenerating ? 'not-allowed' : 'pointer',
              fontWeight: 'bold',
              transition: 'background-color 0.2s'
            }}
          >
            {isGenerating ? 'Génération en cours...' : 'Générer (Solveur)'}
          </button>
        </div>

      </form>
    </div>
  );
};
