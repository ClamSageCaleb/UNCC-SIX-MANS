import React from "react";
import { IQueue, IBallChaser } from "../../types";
import { eel } from "../../App";
import { message, Card, Button, Spin } from "antd";
import PlayerList, { IPlayerListPlayer } from "../PlayerList/PlayerList";
import SyncOutlined from "@ant-design/icons/SyncOutlined";
import ClearOutlined from "@ant-design/icons/ClearOutlined";
import DeleteOutlined from "@ant-design/icons/DeleteOutlined";

interface IQueueProps {
  queue: IQueue;
  reserves: Array<IBallChaser> | undefined;
  updateQueue: () => void;
  updateReserves: () => void;
}

export default function Queue(props: IQueueProps) {
  const [selectedPlayers, setSelectedPlayers] = React.useState<Array<string>>([]);

  function removeSelectedFromQueue() {
    if (props.reserves) {
      let newQueue: IQueue = {...props.queue};
      let newReserves = Array.from(props.reserves);

      selectedPlayers.forEach(selectedPlayer => {
        const queues: Array<{ key: keyof IQueue, list: Array<IBallChaser> }> = [
          {
            key: "queue",
            list: newQueue.queue
          },
          {
            key: "blueTeam",
            list: newQueue.blueTeam
          },
          {
            key: "orangeTeam",
            list: newQueue.orangeTeam
          },
        ];
        let foundSelectedPlayer: IBallChaser | undefined = undefined;
        queues.forEach((playerList) => {
          let newPlayerList = Array.from(playerList.list);
          const index = newPlayerList.findIndex(player => player.name === selectedPlayer);
          if (index >= 0) {
            foundSelectedPlayer = newPlayerList.splice(index, 1)[0];
            switch(playerList.key) {
              case "queue": newQueue.queue = newPlayerList; break;
              case "blueTeam": newQueue.blueTeam = newPlayerList; break;
              case "orangeTeam": newQueue.orangeTeam = newPlayerList; break;
            }
            return;
          }
        });
        if (foundSelectedPlayer) newReserves.push(foundSelectedPlayer);
      });

      setSelectedPlayers([]);

      eel.setReserves(newReserves)((ret: string) => message.success(ret));
      eel.setCurrentQueue(newQueue)((ret: string) => message.success(ret));
      props.updateQueue();
      props.updateReserves();
    }
  }

  function clearQueue() {
    if (props.reserves) {
      let newQueue: IQueue = {...props.queue};
      let newReserves = Array.from(props.reserves);

      const queues: Array<Array<IBallChaser>> = [newQueue.queue, newQueue.blueTeam, newQueue.orangeTeam];
      queues.forEach((playerList) => {
        playerList.forEach(player => {
          newReserves.push(player);
        });
      });
      newQueue.queue = newQueue.blueTeam = newQueue.orangeTeam = [];

      setSelectedPlayers([]);

      eel.setReserves(newReserves)((ret: string) => message.success(ret));
      eel.setCurrentQueue(newQueue)((ret: string) => message.success(ret));
      props.updateQueue();
      props.updateReserves();
    }
  }

  let currentQueueData: Array<IPlayerListPlayer> = [];
  props.queue.queue.forEach(player => {
    currentQueueData.push({
      name: player.name,
      team: "N/A",
      extra: false,
    });
  });
  props.queue.blueTeam.forEach(player => {
    currentQueueData.push({
      name: player.name,
      team: "Blue",
      extra: player.id === props.queue.blueCap.id,
    });
  });
  props.queue.orangeTeam.forEach(player => {
    currentQueueData.push({
      name: player.name,
      team: "Orange",
      extra: player.id === props.queue.orangeCap.id,
    });
  });

  return (
    <Card
      title="Current Queue"
      className="currQueueCard"
      type="inner"
      extra={<Button size="small" icon={<SyncOutlined/>} onClick={props.updateQueue}>Refresh</Button>}
      actions={[
        <Button
          size="small"
          disabled={selectedPlayers.length === 0}
          onClick={() => removeSelectedFromQueue()}
          icon={<DeleteOutlined/>}
        >
          Remove from Queue
        </Button>,
        <Button
          size="small"
          disabled={currentQueueData.length === 0}
          onClick={() => clearQueue()}
          icon={<ClearOutlined/>}
        >
          Clear Queue
        </Button>
      ]}
    >
      {!props.queue && <Spin/>}
      {props.queue && 
        <PlayerList
          players={currentQueueData}
          headerColumns={["Name", "Team", "Captain"]}
          onExtraChange={() => null}
          onSelectedPlayer={(selectedPlayers) => setSelectedPlayers(selectedPlayers)} 
        />
      }
    </Card>
  );
}