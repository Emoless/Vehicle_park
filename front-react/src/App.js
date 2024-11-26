import React, { useState } from 'react';
import './App.css';
import AddDriver from './AddDriver';
import AddTask from './AddTask';
import AddVehicle from './AddVehicle';

function App() {
  const [activeTab, setActiveTab] = useState('driver'); // Хранение активной вкладки

  return (
    <div className="App">
      <h1>Management System</h1>

      {/* Вкладки */}
      <div className="tabs">
        <button
          className={activeTab === 'driver' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('driver')}
        >
          Add Driver
        </button>
        <button
          className={activeTab === 'task' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('task')}
        >
          Add Task
        </button>
        <button
          className={activeTab === 'vehicle' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('vehicle')}
        >
          Add Vehicle
        </button>
      </div>

      {/* Окна, зависящие от активной вкладки */}
      <div className="tab-content">
        {activeTab === 'driver' && (
          <div className="window">
            <AddDriver />
          </div>
        )}
        {activeTab === 'task' && (
          <div className="window">
            <AddTask />
          </div>
        )}
        {activeTab === 'vehicle' && (
          <div className="window">
            <AddVehicle />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
