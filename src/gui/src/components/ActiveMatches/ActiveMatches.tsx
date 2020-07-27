import React from "react";
import { eel } from "../../App";
import {Card, Empty, Spin} from "antd";
import { IActiveMatch } from "../../types";
import PlayerList, { IPlayerListPlayer } from "../PlayerList/PlayerList";

export default function ActiveMatches() {
  const [activeMatches, setActiveMatches] = React.useState<Array<IActiveMatch>>();

  React.useEffect(() => {
    eel.getActiveMatches()((activeMatches: Array<IActiveMatch>) => setActiveMatches(activeMatches));
  }, []);

  if (!activeMatches) {
    return (
      <Card title="Active Matches" className="container">
        <Spin/>
      </Card>
    )
  }
  
  if (activeMatches.length === 0) {
    return (
      <Card title="Active Matches" className="container">
        <Empty/>
      </Card>
    )
  }

  let activeMatchesData: Array<IPlayerListPlayer> = [];
  if (activeMatches) {
    activeMatches[0].blueTeam.forEach(player => {
      activeMatchesData.push({
        name: player,
        team: "Blue",
        extra: activeMatches[0].reportedWinner.player === player,
      });
    });
    activeMatches[0].orangeTeam.forEach(player => {
      activeMatchesData.push({
        name: player,
        team: "Orange",
        extra: activeMatches[0].reportedWinner.player === player,
      });
    });
  }

  return (
    <Card title="Active Matches" className="container">
      {activeMatches.map((match, index) => (
        <Card key={match.blueTeam[0]} type="inner" title={`Match ${index + 1}`} className="innerCard">
          <PlayerList players={activeMatchesData} headerColumns={["Name", "Team", "Reported"]} onExtraChange={() => null} />
        </Card>
      ))}
    </Card>
  );
}