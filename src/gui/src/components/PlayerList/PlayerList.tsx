import React from "react";
import {Select, Checkbox, Typography, Empty} from "antd";
import { IBallChaser } from "../../types";
import "./PlayerList.scss";

const { Option } = Select;
const { Text } = Typography;

interface IPlayerListProps {
  players: Array<IBallChaser | string>;
  headerColumns: Array<string>;
}

export default function PlayerList(props: IPlayerListProps) {

  if (props.players.length === 0) {
    return (
      <Empty/>
    )
  }

  return (
    <>
      <div className="listHeader">
        <Text strong>{props.headerColumns[0]}</Text>
        <Text strong>{props.headerColumns[1]}</Text>
        <Text strong>{props.headerColumns[2]}</Text>
      </div>
      {props.players.map((player: string | IBallChaser) => (
        <div key={typeof player === "string" ? player : player.id} className="player">
          <Text className="playerName">{typeof player === "string" ? player : player.name}</Text>
          <Select className="teamSelect" defaultValue="N/A">
            <Option value="N/A">N/A</Option>
            <Option value="Blue">Blue</Option>
            <Option value="Orange">Orange</Option>
          </Select>
          <Checkbox className="captainCheck"/>
        </div>
      ))}
    </>
  );
}
