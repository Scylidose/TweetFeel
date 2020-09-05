import React, { useState, useEffect } from 'react';
import './css/style.css';

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="App">
      <div>
        <h3>Sample Generated Songs</h3>
        <div>
          <h5>Battle</h5>
        </div>
        <div>
          <h5>Route</h5>
        </div>
        <div>
          <h5>Buildings</h5>
        </div>
      </div>

      <div>
        <h3>Generate a song</h3>
        <div>
          
        </div>
      </div>
    </div>
  );
}

export default App;

