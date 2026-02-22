import React, { useState } from 'react';
import type { GeneratePlanningPayload } from '../types/planning';

interface GeneratePlanningFormProps {
  onSubmit: (payload: GeneratePlanningPayload) => void;
  isGenerating: boolean;
}

export const GeneratePlanningForm: React.FC<GeneratePlanningFormProps> = ({ onSubmit, isGenerating }) => {
  const [dateDebut, setDateDebut] = useState('2026-01-01');
  const [dureeCycle, setDureeCycle] = useState<number>(84);
  const [politiqueId, setPolitiqueId] = useState('pol-1');
  const [agentIds, setAgentIds] = useState<string>('uuid-1, uuid-2'); // Simple comma separated for now

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Basic validation
    if (!dateDebut || !dureeCycle || !politiqueId || !agentIds) {
      alert('Veuillez remplir tous les champs');
      return;
    }

    const payload: GeneratePlanningPayload = {
      date_debut: dateDebut,
      duree_cycle: dureeCycle,
      politique_id: politiqueId,
      agent_ids: agentIds.split(',').map(id => id.trim()).filter(id => id)
    };

    onSubmit(payload);
  };

  return (
    <div style={{ backgroundColor: '#f8fafc', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0', marginBottom: '30px' }}>
      <h3 style={{ marginTop: 0, marginBottom: '15px', color: '#1e293b' }}>Générer un Nouveau Planning</h3>
      <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
          <label htmlFor="dateDebut" style={{ fontSize: '0.9em', fontWeight: 'bold', color: '#475569' }}>Date de début</label>
          <input 
            type="date" 
            id="dateDebut"
            value={dateDebut} 
            onChange={(e) => setDateDebut(e.target.value)}
            disabled={isGenerating}
            style={{ padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
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
            style={{ padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
          />
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
          <label htmlFor="politiqueId" style={{ fontSize: '0.9em', fontWeight: 'bold', color: '#475569' }}>Politique de conformité</label>
          <select 
            id="politiqueId"
            value={politiqueId} 
            onChange={(e) => setPolitiqueId(e.target.value)}
            disabled={isGenerating}
            style={{ padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1', backgroundColor: 'white' }}
          >
            <option value="pol-1">Politique Standard (11h repos)</option>
            <option value="pol-2">Politique Renforcée</option>
          </select>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
          <label htmlFor="agentIds" style={{ fontSize: '0.9em', fontWeight: 'bold', color: '#475569' }}>Agents (IDs séparés par des virgules)</label>
          <input 
            type="text" 
            id="agentIds"
            value={agentIds} 
            onChange={(e) => setAgentIds(e.target.value)}
            disabled={isGenerating}
            placeholder="uuid-1, uuid-2"
            style={{ padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
          />
        </div>

        <div style={{ display: 'flex', alignItems: 'flex-end' }}>
          <button 
            type="submit" 
            disabled={isGenerating}
            style={{ 
              backgroundColor: isGenerating ? '#94a3b8' : '#2563eb', 
              color: 'white', 
              padding: '10px 15px', 
              borderRadius: '4px', 
              border: 'none',
              cursor: isGenerating ? 'not-allowed' : 'pointer',
              fontWeight: 'bold',
              width: '100%',
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
