import { Team } from "../../types/BallChaser";
import { NotionSelectElement, NotionTextElement } from "../helpers/NotionTypes";

export interface ActiveMatchPageProperties {
  ID: NotionTextElement;
  MatchID: NotionTextElement;
  Team: NotionSelectElement<Team>;
  Reported: NotionSelectElement<Team>;
}

export interface UpdateActiveMatchOptions {
  id?: string;
  matchId?: string;
  team?: Team;
  reported?: Team | null;
}

export interface PlayerInActiveMatch {
  id: string;
  team: Team;
  reported: Team | null;
  matchId: string;
}
