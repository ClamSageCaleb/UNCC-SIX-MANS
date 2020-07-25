import React from "react";
import { eel } from "../../App";
import { IQueue } from "../../types";
import PlayerList from "../PlayerList/PlayerList";
import { Card, Spin } from "antd";
import "./CurrentQueue.scss";

export default function CurrentQueue() {
  const [queue, setQueue] = React.useState<IQueue>();

  React.useEffect(() => {
    eel.getCurrentQueue()((currQuue: IQueue) => setQueue(currQuue));
  }, []);

  return (
    <Card title="Current Queue" className="container">
      {!queue && <Spin/>}
      {queue && <PlayerList players={queue.queue} headerColumns={["Name", "Team", "Captain"]} />}
    </Card>
  );
}