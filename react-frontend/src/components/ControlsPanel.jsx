import { useState, useEffect } from 'react';

export default function ControlsPanel({ serverUrl }) {
  const [params, setParams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchParams = async () => {
      try {
        const response = await fetch(`${serverUrl}/current_effect`);
        const data = await response.json();

        if (response.ok) {
          setParams(data.effect_parameters || []);
        } else {
          setError(data.error || 'Failed to fetch effect parameters');
        }
      } catch (err) {
        setError('Network error while fetching parameters');
      } finally {
        setLoading(false);
      }
    };

    fetchParams();
  }, [serverUrl]);

  const handleParamChange = async (paramName, value) => {
    try {
      const response = await fetch(`${serverUrl}/control/update_param`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ param_name: paramName, value })
      });

      if (!response.ok) {
        throw new Error('Failed to update parameter');
      }
    } catch (err) {
      console.error('Parameter update error:', err);
    }
  };

  if (loading) {
    return <div>Loading effect parameters...</div>;
  }

  if (error) {
    return <div style={{color: 'red'}}>{error}</div>;
  }
  const [params, setParams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchParams = async () => {
      try {
        const response = await fetch(`${serverUrl}/current_effect`);
        const data = await response.json();

        if (response.ok) {
          setParams(data.effect_parameters || []);
        } else {
          setError(data.error || 'Failed to fetch effect parameters');
        }
      } catch (err) {
        setError('Network error while fetching parameters');
      } finally {
        setLoading(false);
      }
    };

    fetchParams();
  }, [serverUrl]);

  const handleParamChange = async (paramName, value) => {
    try {
      const response = await fetch(`${serverUrl}/control/update_param`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ param_name: paramName, value })
      });

      if (!response.ok) {
        throw new Error('Failed to update parameter');
      }
    } catch (err) {
      console.error('Parameter update error:', err);
    }
  };

  if (loading) {
    return <div>Loading effect parameters...</div>;
  }

  if (error) {
    return <div style={{color: 'red'}}>{error}</div>;
  }

  return (
    <div>
      <h3>Effect Controls</h3>
      {params.map((param, index) => (
        <div key={index}>
          <label>{param.name} ({param.type})</label>
          {param.type === 'int' ? (
            <input
              type="range"
              min={param.min}
              max={param.max}
              step={param.step}
              value={param.value}
              onChange={(e) => handleParamChange(param.name, parseInt(e.target.value))}
            />
          ) : (
            <input
              type="number"
              value={param.value}
              onChange={(e) => handleParamChange(param.name, parseFloat(e.target.value))}
            />
          )}
        </div>
      ))}
    </div>
  );
};

export default ControlsPanel;