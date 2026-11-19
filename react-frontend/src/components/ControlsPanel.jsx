import { useState, useEffect } from 'react';

export default function ControlsPanel() {
  const [params, setParams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchParams = async () => {
      try {
        const response = await fetch('/api/current_effect');
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
  }, []);


const handleNextEffect = () => {
    sendControlCommand('next_effect');
  };


  const handleReset = () => {
    sendControlCommand('reset');
  };


const sendControlCommand = (action) => {
    fetch(`/api/control/${action}`)
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          console.log(`Command ${action} executed successfully`);
        } else {
          console.error('Error executing command:', data.error);
        }
      })
      .catch(error => {
        console.error('Error sending command:', error);
      });
  };



 const handlePrevEffect = () => {
    sendControlCommand('prev_effect');
  };


  const handleParamChange = async (paramName, value) => {
    try {
      const response = await fetch('/api/control/update_param', {
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
           <button onClick={handlePrevEffect} className="control-btn">Previous Effect</button>
         <button onClick={handleNextEffect} className="control-btn">Next Effect</button>
         <button onClick={handleReset} className="control-btn">Reset</button>

        </div>
      ))}
    </div>
  );
}
