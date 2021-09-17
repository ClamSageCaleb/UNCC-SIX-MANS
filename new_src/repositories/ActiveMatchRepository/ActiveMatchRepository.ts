import { BallChaser, Team } from "../../types/common";
import generateRandomId from "../../utils/randomId";
import NotionClient from "../helpers/NotionClient";
import { ActiveMatchPageProperties, PlayerInActiveMatch, UpdateActiveMatchOptions } from "./types";

export class ActiveMatchRepository {
  #Client: NotionClient;

  constructor() {
    const databaseId = process.env.notion_active_match_id;

    if (!databaseId) {
      throw new Error("No environment variable named notion_active_match_id.");
    } else {
      this.#Client = new NotionClient(databaseId);
    }
  }

  async addActiveMatch(ballChasers: Array<BallChaser>): Promise<void> {
    const insertPromises: Array<Promise<void>> = [];
    const matchId = generateRandomId();

    for (const ballChaser of ballChasers) {
      if (!ballChaser.team) {
        throw new Error(`Cannot add a player to an active match without a team: ${ballChaser.name}.`);
      }

      const newActiveMatchPage: ActiveMatchPageProperties = {
        ID: NotionClient.notionTextElementFromText(ballChaser.id),
        MatchID: NotionClient.notionTextElementFromText(matchId),
        Reported: NotionClient.notionSelectElementFromValue<Team>(null),
        Team: NotionClient.notionSelectElementFromValue<Team>(ballChaser.team),
      };

      insertPromises.push(this.#Client.insert(newActiveMatchPage));
    }

    await Promise.all(insertPromises);
  }

  async updateAllPlayersInActiveMatch(playerInMatchId: string, updates: UpdateActiveMatchOptions): Promise<void> {
    const playerInActiveMatchPage = await this.#Client.getById(playerInMatchId);

    if (!playerInActiveMatchPage) {
      throw new Error(`Player with ID: ${playerInMatchId} is not in an active match.`);
    }

    const existingPlayerActiveMatchProps = playerInActiveMatchPage.properties as unknown as ActiveMatchPageProperties;

    const allActiveMatchPages = await this.#Client.getAll({
      filter: {
        property: "MatchID",
        text: {
          equals: NotionClient.textFromNotionTextElement(existingPlayerActiveMatchProps.MatchID),
        },
      },
    });

    const updatePromises: Array<Promise<void>> = [];
    for (const activeMatchPage of allActiveMatchPages) {
      const activeMatchProps = activeMatchPage.properties as unknown as ActiveMatchPageProperties;

      const propertiesUpdate: ActiveMatchPageProperties = {
        ID: updates.id ? NotionClient.notionTextElementFromText(updates.id) : activeMatchProps.ID,
        MatchID: updates.matchId ? NotionClient.notionTextElementFromText(updates.matchId) : activeMatchProps.MatchID,
        Reported: updates.reported ? NotionClient.notionSelectElementFromValue<Team>(null) : activeMatchProps.Reported,
        Team: updates.team ? NotionClient.notionSelectElementFromValue<Team>(updates.team) : activeMatchProps.Team,
      };

      updatePromises.push(this.#Client.update(activeMatchPage.id, propertiesUpdate));
    }

    await Promise.all(updatePromises);
  }

  async removeAllPlayersInActiveMatch(playerInMatchId: string): Promise<void> {
    const playerInActiveMatchPage = await this.#Client.getById(playerInMatchId);

    if (!playerInActiveMatchPage) {
      throw new Error(`Player with ID: ${playerInMatchId} is not in an active match.`);
    }

    const activeMatchProps = playerInActiveMatchPage.properties as unknown as ActiveMatchPageProperties;

    await this.#Client.findAllAndRemove({
      filter: {
        property: "MatchID",
        text: {
          equals: NotionClient.textFromNotionTextElement(activeMatchProps.MatchID),
        },
      },
    });
  }

  async getAllPlayersInActiveMatch(playerInMatchId: string): Promise<Array<PlayerInActiveMatch>> {
    const playerInActiveMatchPage = await this.#Client.getById(playerInMatchId);

    if (!playerInActiveMatchPage) {
      throw new Error(`Player with ID: ${playerInMatchId} is not in an active match.`);
    }

    const existingPlayerActiveMatchProps = playerInActiveMatchPage.properties as unknown as ActiveMatchPageProperties;

    const allActiveMatchPages = await this.#Client.getAll({
      filter: {
        property: "MatchID",
        text: {
          equals: NotionClient.textFromNotionTextElement(existingPlayerActiveMatchProps.MatchID),
        },
      },
    });

    return allActiveMatchPages.map((page) => {
      const pageProps = page.properties as unknown as ActiveMatchPageProperties;

      const playerTeam = NotionClient.valueFromNotionSelectElement<Team>(pageProps.Team);
      if (!playerTeam) {
        throw new Error(
          `Player with ID: ${pageProps.ID.rich_text[0].text.content} is in an active match but not on a team`
        );
      }

      return {
        id: NotionClient.textFromNotionTextElement(pageProps.ID),
        matchId: NotionClient.textFromNotionTextElement(pageProps.MatchID),
        reported: NotionClient.valueFromNotionSelectElement<Team>(pageProps.Reported),
        team: playerTeam,
      };
    });
  }
}

export default new ActiveMatchRepository();
