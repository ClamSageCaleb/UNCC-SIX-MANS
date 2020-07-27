import React from "react";
import {Select, Checkbox, Typography, Empty, Row, Col} from "antd";
import { Team } from "../../types";

const { Option } = Select;
const { Text } = Typography;

export interface IPlayerListPlayer {
  name: string;
  team: Team;
  extra: boolean;
}

interface IPlayerListProps {
  players: Array<IPlayerListPlayer>;
  headerColumns: Array<string>;
  onSelectedPlayer?: (player: Array<string>) => void;
  onExtraChange: (player: string, newValue: boolean) => void;
}

export default function PlayerList(props: IPlayerListProps) {
  const [selectedPlayers, setSelectedPlayers] = React.useState<Array<string>>([]);

  if (props.players.length === 0)
    return <Empty/>;

  function handlePlayerSelectChange(player: string, checked: boolean) {
    let newSelectedPlayers;

    if (checked)
      newSelectedPlayers = selectedPlayers.concat([player]);
    else
      newSelectedPlayers = selectedPlayers.filter(selected => selected !== player);

    if (props.onSelectedPlayer) props.onSelectedPlayer(newSelectedPlayers);
    setSelectedPlayers(newSelectedPlayers);
  }

  return (
    <>
      <Row gutter={[10, 16]}>
        <Col span={9} offset={2}>
          <Text strong>{props.headerColumns[0]}</Text>
        </Col>
        <Col span={9}>
          <Text strong>{props.headerColumns[1]}</Text>
        </Col>
        <Col span={4}>
          <Text strong>{props.headerColumns[2]}</Text>
        </Col>
      </Row>
      {props.players.map((player) => (
        <Row key={player.name} gutter={[10, 12]} justify="center" align="middle">
          <Col span={2}>
            {props.onSelectedPlayer && 
              <Checkbox onChange={(e) => handlePlayerSelectChange(player.name, e.target.checked)}/>
            }
          </Col>
          <Col span={9}>
            <Text>{player.name}</Text>
          </Col>
          <Col span={9} >
            <Select defaultValue={player.team} style={{width: "80%"}}>
              <Option value="N/A">N/A</Option>
              <Option value="Blue">Blue</Option>
              <Option value="Orange">Orange</Option>
            </Select>
          </Col>
          <Col span={4} >
            <Checkbox
              checked={player.extra}
              onChange={(e) => props.onExtraChange(player.name, e.target.checked)}
              style={{margin: "auto"}}
            />
          </Col>
        </Row>
      ))}
    </>
  );
}
