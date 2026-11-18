import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [cameraStatus, setCameraStatus] = useState('connecting');
  const [panelVisible, setPanelVisible] = useState(true);
  const [currentEffect, setCurrentEffect] = useState('None');
  const [effectParams, setEffectParams] = useState([]);
  const [serverUrl, setServerUrl] = useState(
  () => `${window.location.protocol}//${window.location.hostname}:5000`
);

  useEffect(() => {
    // Get initial status from server
    fetch(`${serverUrl}/health`)
      .then(response => response.json())
      .then(data => {
        setCameraStatus(data.camera_connected ? 'connected' : 'disconnected');
        setCurrentEffect(data.current_effect || 'None');
      })
      .catch(error => {
        console.error('Error fetching health status:', error);
        setCameraStatus('error');
      });

    // Fetch current effect info periodically
    const interval = setInterval(() => {
      fetch(`${serverUrl}/current_effect`)
        .then(response => response.json())
        .then(data => {
          setCurrentEffect(data.current_effect || 'None');
          setEffectParams(data.effect_parameters || []);
        })
        .catch(error => {
          console.error('Error fetching effect info:', error);
        });
    }, 1000);

    return () => clearInterval(interval);
  }, [serverUrl]);

  const sendControlCommand = (action) => {
    fetch(`${serverUrl}/control/${action}`)
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

  const handleTogglePanel = () => {
    sendControlCommand('toggle_panel');
    setPanelVisible(!panelVisible);
  };

  const handleNextEffect = () => {
    sendControlCommand('next_effect');
  };

  const handlePrevEffect = () => {
    sendControlCommand('prev_effect');
  };

  const handleReset = () => {
    sendControlCommand('reset');
  };

  const handleParamAdjust = (paramIndex, direction) => {
    // This would normally be implemented on the backend to handle parameter changes
    console.log(`Adjusting param ${paramIndex} ${direction}`);
    // For now we just log it 
  };

  return (
    <div className="app">
      <div className="header">
        
        <div className="status">
          <span className={`status-indicator ${cameraStatus}`}>
            {cameraStatus === 'connected' ? '✓ Camera Connected' : 
             cameraStatus === 'disconnected' ? '✗ No Camera' : 
             '⚠ Error'}
          </span>
            </div>
            <div className="parameter-controls">
              {effectParams.map((param, index) => (
                <div key={index} className="param-group">
                  <span>{param.name}</span>
                  <button onClick={() => handleParamAdjust(index, 'increase')}>↑</button>
                  <button onClick={() => handleParamAdjust(index, 'decrease')}>↓</button>
                </div>
              ))}
            </div>
          </div>

      <div className="video-container">
        <img 
          src={`${serverUrl}/video_feed`} 
          alt="Camera feed from Old TV Mirror" 
          className="video-feed"
        />
        
        {panelVisible && (
          <div className="overlay-panel">
            <h2>Effect Controls</h2>
            <p>Current Effect: {currentEffect}</p>
            
        <div className="effect-controls">
          <button onClick={handlePrevEffect} className="control-btn">Previous Effect</button>
          <button onClick={handleNextEffect} className="control-btn">Next Effect</button>
          <button onClick={handleReset} className="control-btn">Reset</button>
        </div>
          </div>
        )}
      </div>

      <div className="controls">
        <button onClick={handlePrevEffect} className="control-btn">Previous Effect</button>
        <button onClick={handleTogglePanel} className={`control-btn ${panelVisible ? 'active' : ''}`}>
          {panelVisible ? 'Hide Panel' : 'Show Panel'}
        </button>
        <button onClick={handleNextEffect} className="control-btn">Next Effect</button>
        <button onClick={handleReset} className="control-btn">Reset</button>
      </div>

      <div className="server-info">
        <p>Connected to: {serverUrl}</p>
        <input 
          type="text" 
          value={serverUrl}
          onChange={(e) => setServerUrl(e.target.value)}
          placeholder="Enter server URL"
          className="url-input"
        />
      </div>
    </div>
  );
}

export default App;
