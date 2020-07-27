import React from "react";
import { IQueue, IBallChaser } from "../../types";
import { eel } from "../../App";
import { message, Card, Button, Popconfirm, Empty, Checkbox } from "antd";
import NewReservePopout from "./NewReservePopout";
import PlusCircleOutlined from "@ant-design/icons/PlusCircleOutlined";
import DeleteOutlined from "@ant-design/icons/DeleteOutlined";
import UserAddOutlined from "@ant-design/icons/UserAddOutlined";

interface IReservesProps {
  queue: IQueue | undefined;
  reserves: Array<IBallChaser>;
  updateQueue: () => void;
  updateReserves: () => void;
}

export default function Reserves(props: IReservesProps) {
  const [selectedReserves, setSelectedReserves] = React.useState<Array<string>>([]);
  const [showNewReserve, setShowNewReserve] = React.useState<boolean>(false);

  let reserveCheckboxes: Array<{label: string, value: string}> = [];
  props.reserves.map((reserve) => (
    reserveCheckboxes.push({
      label: reserve.name,
      value: reserve.id
    })
  ));

  function handleNewReserve(newReserve: IBallChaser) {
    let newReserves = Array.from(props.reserves ?? []);
    newReserves.push(newReserve);
    eel.setReserves(newReserves)((ret: string) => message.success(ret));
    setShowNewReserve(false);
    props.updateReserves();
  }

  function handleRemoveReserves() {
    const newReserves = props.reserves.filter((reserve) => !selectedReserves.includes(reserve.id));
    eel.setReserves(newReserves)((ret: string) => message.success(ret));
    props.updateReserves();
  }

  function addReservesToQueue() {
    if (props.queue){
      let newQueue: IQueue = {...props.queue};
      let newReserves = Array.from(props.reserves);

      selectedReserves.map(selectedReserve => {
        const playerToAdd = newReserves.findIndex((reserve) => reserve.id === selectedReserve);
        if (playerToAdd >= 0){
          newQueue.queue.push(newReserves.splice(playerToAdd, 1)[0]);
        }
        return playerToAdd;
      });

      setSelectedReserves([]);

      eel.setReserves(newReserves)((ret: string) => message.success(ret));
      eel.setCurrentQueue(newQueue)((ret: string) => message.success(ret));
      props.updateReserves();
      props.updateQueue();
    }
  }

  return (
    <>
      <Card
        title="Reserves"
        className="currQueueCard"
        type="inner"
        extra={
          <Button
            icon={<UserAddOutlined/>}
            onClick={() => setShowNewReserve(true)}
            size="small"
          >
            Add Reserve
          </Button>
        }
        actions={[
          <Button
            key="addToQueue"
            size="small"
            onClick={() => addReservesToQueue()}
            disabled={selectedReserves.length === 0}
            icon={<PlusCircleOutlined/>}
          >
            Add to Queue
          </Button>,
          <Popconfirm
            title="Are you sure you want to remove these players from the reserve?"
            okText="Yes"
            cancelText="Cancel"
            onConfirm={handleRemoveReserves}
          >
            <Button
              key="removeReserve"
              size="small"
              disabled={selectedReserves.length === 0}
              icon={<DeleteOutlined/>}
            >
              Remove from Reserves
            </Button>
          </Popconfirm>
        ]}
      >
        {props.reserves.length === 0 && <Empty description="No Reserves" />}
        {props.reserves.length > 0  && 
          <Checkbox.Group
            options={reserveCheckboxes}
            onChange={(checkedValues) => setSelectedReserves(checkedValues as Array<string>)} 
          />
        }
      </Card>
      <NewReservePopout
        onClose={() => setShowNewReserve(false)}
        open={showNewReserve}
        onNewReserve={handleNewReserve}
      />
    </>
  )
}