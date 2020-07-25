import React from "react";
import { eel } from "../../App";
import {Card, Empty, Spin} from "antd";
import { IActiveMatch } from "../../types";
import PlayerList from "../PlayerList/PlayerList";
import "./ActiveMatches.scss";

export default function ActiveMatches() {
  const [activeMatches, setActiveMatches] = React.useState<Array<IActiveMatch>>();

  React.useEffect(() => {
    eel.getActiveMatches()((activeMatches: Array<IActiveMatch>) => setActiveMatches(activeMatches));
  }, []);

  if (!activeMatches) {
    return (
      <Card title="Active Matches" className="outerCard">
        <Spin/>
      </Card>
    )
  }
  
  if (activeMatches.length === 0) {
    return (
      <Card title="Active Matches" className="outerCard">
        <Empty/>
      </Card>
    )
  }

  return (
    <Card title="Active Matches" className="outerCard">
      {activeMatches.map((match, index) => (
        <Card key={match.blueTeam[0]} type="inner" title={`Match ${index + 1}`} className="innerCard">
          <PlayerList players={match.blueTeam.concat(match.orangeTeam)} headerColumns={["Name", "Team", "Reported"]} />
        </Card>
      ))}
    </Card>
  );
}