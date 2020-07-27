import React from 'react';
import './App.css';
import CurrentQueue from './components/CurrentQueue/CurrentQueue';
import ActiveMatches from './components/ActiveMatches/ActiveMatches';
import Leaderboard from './components/Leaderboard/Leaderboard';
import ConfigOptions from './components/ConfigOptions/ConfigOptions';
import { Row, Col } from 'antd';

// Point Eel web socket to the instance
export const eel = window.eel
eel.set_host('ws://localhost:8080')

function App() {

  return (
    <>
      <Row justify="space-around" style={{margin: "3em"}}>
        <Col span={12}>
          <CurrentQueue/>
        </Col>
        <Col span={11}>
          <ActiveMatches/>
        </Col>
      </Row>
      <Row justify="space-around" style={{margin: "3em"}}>
        <Col span={14}>
          <Leaderboard/>
        </Col>
        <Col span={8}>
          <ConfigOptions/>
        </Col>
      </Row>
    </>
  );
}

export default App;
