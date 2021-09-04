import BallChaser from "../../types/BallChaser";
import { BallChaserPageProperties, UpdateBallChaserOptions } from "./types";
import { DateTime } from "luxon";
import NotionClient from "../helpers/NotionClient";

export class QueueRepository {
  #Client: NotionClient;

  constructor() {
    const databaseId = process.env.notion_queue_id;

    if (!databaseId) {
      throw new Error("No environment variable named notion_queue_id.");
    } else {
      this.#Client = new NotionClient(databaseId);
    }
  }

  /**
   * Retrieves a BallChaser with a specific Discord ID
   * @param id Discord ID of the BallChaser to retrieve
   * @returns A BallChaser object if the player is found, otherwise null
   */
  async getBallChaserInQueue(id: string): Promise<BallChaser | null> {
    const ballChaserPage = await this.#Client.getById(id);

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
    const ballChaserPages = await this.#Client.getAll();

    return ballChaserPages.map((page) => {
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
    const ballChaserPage = await this.#Client.getById(id);

    if (!ballChaserPage) {
      throw new Error(`Cannot remove BallChaser. No BallChaser with the ID ${id} was found.`);
    }

    await this.#Client.remove(ballChaserPage.id);
  }

  /**
   * Removes all BallChasers currently in the queue.
   */
  async removeAllBallChasersFromQueue(): Promise<void> {
    const allBallChasers = await this.getAllBallChasersInQueue();
    const allBallChaserIds = allBallChasers.map((ballChaser) => ballChaser.id);

    await this.#Client.remove(allBallChaserIds);
  }

  /**
   * Function for updating an existing BallChaser in the queue.
   * @param options BallChaser fields to update. ID field is required for retrieving the BallChaser object to update.
   */
  async updateBallChaserInQueue({ id, ...options }: UpdateBallChaserOptions): Promise<void> {
    const ballChaserPage = await this.#Client.getById(id);

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

    await this.#Client.update(ballChaserPage.id, propertiesUpdate);
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
      QueueTime: { date: { start: ballChaserToAdd.queueTime ? ballChaserToAdd.queueTime.toISO() : "" } },
      Team: { select: ballChaserToAdd.team ? { name: ballChaserToAdd.team } : null },
      isCap: { checkbox: ballChaserToAdd.isCap },
    };

    await this.#Client.insert(newBallChaserProperties);
  }
}

export default new QueueRepository();
