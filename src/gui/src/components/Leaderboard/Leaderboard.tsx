import React from "react";
import { IRankedPlayer } from "../../types";
import { eel } from "../../App";
import { Table, Card } from "antd";

export default function Leaderboard() {
  const [leaderboard, setLeaderboard] = React.useState<Array<IRankedPlayer>>();

  React.useEffect(() => {
    eel.getLeaderboard()((players: Array<IRankedPlayer>) => setLeaderboard(players));
  }, []);

  const columns = [
    {
      title: "Name",
      dataIndex: "Name",
      key: "Name",
    },
    {
      title: "Wins",
      dataIndex: "Wins",
      key: "Wins",
    },
    {
      title: "Losses",
      dataIndex: "Losses",
      key: "Losses",
    },
    {
      title: "Matches Played",
      dataIndex: "Matches Played",
      key: "Matches Played",
    },
    {
      title: "Win Perc",
      dataIndex: "Win Perc",
      key: "Win Perc",
    },
  ]

  return (
    <Card title="Leaderboard">
      <Table
        size="small"
        rowKey={(item) => item.Name}
        dataSource={leaderboard}
        columns={columns}
        pagination={false}
        scroll={{y: 300}} 
      />
    </Card>
  )
}