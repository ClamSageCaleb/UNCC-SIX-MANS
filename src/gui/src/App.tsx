import React from 'react';
import './App.css';
import CurrentQueue from './components/CurrentQueue/CurrentQueue';
import ActiveMatches from './components/ActiveMatches/ActiveMatches';
import Leaderboard from './components/Leaderboard/Leaderboard';
import ConfigOptions from './components/ConfigOptions/ConfigOptions';

// Point Eel web socket to the instance
export const eel = window.eel
eel.set_host('ws://localhost:8080')

function App() {
  return (
    <div>
      <CurrentQueue/>
      <ActiveMatches/>
      <Leaderboard/>
      <ConfigOptions/>
    </div>
  );
}

export default App;
