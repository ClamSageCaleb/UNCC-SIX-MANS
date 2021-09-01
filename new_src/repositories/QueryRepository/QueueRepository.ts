import { Client as NotionClient } from "@notionhq/client";
import {
  DatabasesQueryParameters,
  DatabasesQueryResponse,
  InputPropertyValueMap,
} from "@notionhq/client/build/src/api-endpoints";
import { Page } from "@notionhq/client/build/src/api-types";
import BallChaser from "../../types/BallChaser";
import { BallChaserPageProperties, UpdateBallChaserOptions } from "./types";
import { DateTime } from "luxon";

class QueueRepository {
  #notionClient: NotionClient;
  #databaseId: string;
  #queryQueueDatabase: (args?: Omit<DatabasesQueryParameters, "database_id">) => Promise<DatabasesQueryResponse>;

  constructor() {
    this.#notionClient = new NotionClient({ auth: process.env.notion_token });

    const databaseId = process.env.notion_queue_id;
    if (!databaseId) {
      throw new Error("No environment variable named notion_queue_id.");
    } else {
      this.#databaseId = databaseId;
      this.#queryQueueDatabase = (args) => this.#notionClient.databases.query({ database_id: databaseId, ...args });
    }
  }

  async #getBallChaserPage(id: string): Promise<Page | null> {
    const ballChaserPage = await this.#queryQueueDatabase({
      filter: {
        property: "ID",
        text: {
          equals: id,
        },
      },
    });

    if (ballChaserPage.results.length === 0) {
      return null;
    } else if (ballChaserPage.results.length > 1) {
      throw new Error(`More than one player found with the ID ${id}.`);
    } else {
      return ballChaserPage.results[0];
    }
  }

  /**
   * Retrieves a BallChaser with a specific Discord ID
   * @param id Discord ID of the BallChaser to retrieve
   * @returns A BallChaser object if the player is found, otherwise null
   */
  async getBallChaserInQueue(id: string): Promise<BallChaser | null> {
    const ballChaserPage = await this.#getBallChaserPage(id);

    if (ballChaserPage) {
      const properties = ballChaserPage.properties as unknown as BallChaserPageProperties;

      return new BallChaser({
        id: properties.ID.rich_text[0].text.content,
        isCap: properties.isCap.checkbox,
        mmr: properties.MMR.number,
        name: properties.Name.rich_text[0].text.content,
        queueTime: DateTime.fromISO(properties.QueueTime.date.start),
        team: properties.Team.select ? properties.Team.select.name : undefined,
      });
    } else {
      return null;
    }
  }

  /**
   * Retrieves all BallChasers in the queue
   * @returns A list of all BallChasers currently in the queue
   */
  async getAllBallChasersInQueue(): Promise<Array<BallChaser>> {
    const ballChaserPages = await this.#queryQueueDatabase();

    return ballChaserPages.results.map((page) => {
      const properties = page.properties as unknown as BallChaserPageProperties;

      return new BallChaser({
        id: properties.ID.rich_text[0].text.content,
        isCap: properties.isCap.checkbox,
        mmr: properties.MMR.number,
        name: properties.Name.rich_text[0].text.content,
        queueTime: DateTime.fromISO(properties.QueueTime.date.start),
        team: properties.Team.select ? properties.Team.select.name : undefined,
      });
    });
  }

  /**
   * Removes the BallChaser from the queue with the specified ID
   * @param id Discord ID of the BallChaser to remove from the queue
   */
  async removeBallChaserFromQueue(id: string): Promise<void> {
    const ballChaserPage = await this.#getBallChaserPage(id);

    if (!ballChaserPage) {
      throw new Error(`Cannot remove BallChaser. No BallChaser with the ID ${id} was found.`);
    }

    // according to the docs archiving a page is the same as deleting it
    // https://developers.notion.com/reference/archive-delete-a-page
    await this.#notionClient.pages.update({
      archived: true,
      page_id: ballChaserPage.id,
      properties: {},
    });
  }

  /**
   * Removes all BallChasers currently in the queue.
   */
  async removeAllBallChasersFromQueue(): Promise<void> {
    const allBallChasers = await this.getAllBallChasersInQueue();

    const removeBallChaserPromises: Array<Promise<void>> = [];
    for (let i = 0; i < allBallChasers.length; i++) {
      const removeBallChaserPromise = this.removeBallChaserFromQueue(allBallChasers[i].id);
      removeBallChaserPromises.push(removeBallChaserPromise);
    }

    await Promise.all(removeBallChaserPromises);
  }

  /**
   * Function for updating an existing BallChaser in the queue.
   * @param options BallChaser fields to update. ID field is required for retrieving the BallChaser object to update.
   */
  async updateBallChaserInQueue({ id, ...options }: UpdateBallChaserOptions): Promise<void> {
    const ballChaserPage = await this.#getBallChaserPage(id);

    if (!ballChaserPage) {
      throw new Error(`Cannot update BallChaser. No BallChaser with the ID ${id} was found.`);
    }

    const existingBallChaserProps = ballChaserPage.properties as unknown as BallChaserPageProperties;
    const propertiesUpdate: BallChaserPageProperties = {
      ID: { rich_text: [{ text: { content: id }, type: "text" }] },
      MMR: options.mmr ? { number: options.mmr } : existingBallChaserProps.MMR,
      Name: options.name
        ? { rich_text: [{ text: { content: options.name }, type: "text" }] }
        : existingBallChaserProps.Name,
      QueueTime: options.queueTime ? { date: { start: options.queueTime.toISO() } } : existingBallChaserProps.QueueTime,
      Team: options.team ? { select: { name: options.team } } : existingBallChaserProps.Team,
      isCap: options.isCap ? { checkbox: options.isCap } : existingBallChaserProps.isCap,
    };

    await this.#notionClient.pages.update({
      archived: false,
      page_id: id,
      properties: propertiesUpdate as unknown as InputPropertyValueMap,
    });
  }

  /**
   * Adds a new BallChaser to the queue.
   * @param ballChaserToAdd New BallChaser object to add to the queue.
   */
  async addBallChaserToQueue(ballChaserToAdd: BallChaser): Promise<void> {
    const ballChaserAlreadyInQueue = await this.getBallChaserInQueue(ballChaserToAdd.id);

    if (ballChaserAlreadyInQueue) {
      throw new Error(`BallChaser with the ID ${ballChaserToAdd.id} is already in the queue.`);
    }

    const newBallChaserProperties: BallChaserPageProperties = {
      ID: { rich_text: [{ text: { content: ballChaserToAdd.id }, type: "text" }] },
      MMR: { number: ballChaserToAdd.mmr },
      Name: { rich_text: [{ text: { content: ballChaserToAdd.name }, type: "text" }] },
      QueueTime: { date: { start: DateTime.now().plus({ minutes: 60 }).toISO() } },
      Team: { select: ballChaserToAdd.team ? { name: ballChaserToAdd.team } : null },
      isCap: { checkbox: ballChaserToAdd.isCap },
    };

    await this.#notionClient.pages.create({
      parent: { database_id: this.#databaseId },
      properties: newBallChaserProperties as unknown as InputPropertyValueMap,
    });
  }
}

export default new QueueRepository();
