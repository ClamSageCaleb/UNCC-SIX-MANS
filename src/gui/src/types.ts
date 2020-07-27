export type Team = "Blue" | "Orange" | "N/A";

export interface IBallChaser {
  name: string;
  id: string;
}

export interface IQueue {
  blueCap: IBallChaser;
  blueTeam: Array<IBallChaser>;
  orangeCap: IBallChaser;
  orangeTeam: Array<IBallChaser>;
  queue: Array<IBallChaser>;
  timeReset: number;
}

export interface IActiveMatch {
  reportedWinner: {
    player: string;
    winningTeam: Team;
  };
  blueTeam: Array<string>;
  orangeTeam: Array<string>;
}

export interface IRankedPlayer {
  Name: string;
  Wins: number;
  Losses: number;
  "Matches Played": number;
  "Win Perc": number;
}

export interface IConfig {
  aws_access_key_id: string;
  aws_secret_access_key: string;
  token: string;
}
