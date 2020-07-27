import React from "react";
import { eel } from "../../App";
import { IQueue, IBallChaser } from "../../types";
import { Card, Spin, Row, Col } from "antd";
import Queue from "./Queue";
import Reserves from "./Reserves";

export default function CurrentQueue() {
  const [queue, setQueue] = React.useState<IQueue>();
  const [reserves, setReserves] = React.useState<Array<IBallChaser>>();

  const getReserves = () => eel.getReserves()((currReserves: Array<IBallChaser>) => setReserves(currReserves));
  const getCurrentQueue = () => eel.getCurrentQueue()((currQuue: IQueue) => setQueue(currQuue));

  React.useEffect(() => {
    getCurrentQueue();
    getReserves();
  }, []);

  return (
    <>
      <Card title="Queue" className="container">
        <Row gutter={16}>
          <Col span={12}>
            {queue && <Queue
              queue={queue}
              reserves={reserves}
              updateQueue={getCurrentQueue}
              updateReserves={getReserves}
            />}
            {!queue && <Spin/>}
          </Col>
          <Col span={12}>
            {reserves && <Reserves
              queue={queue}
              reserves={reserves}
              updateQueue={getCurrentQueue}
              updateReserves={getReserves}
            />}
            {!reserves && <Spin/>}
          </Col>
        </Row>
      </Card>
    </>
  );
}