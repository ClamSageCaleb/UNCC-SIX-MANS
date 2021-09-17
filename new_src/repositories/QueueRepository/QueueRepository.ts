import { BallChaser, Team } from "../../types/common";
import { BallChaserPageProperties, UpdateBallChaserOptions } from "./types";
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

      return {
        id: NotionClient.textFromNotionTextElement(properties.ID),
        isCap: NotionClient.boolFromNotionBooleanElement(properties.isCap),
        mmr: NotionClient.numberFromNotionNumberElement(properties.MMR),
        name: NotionClient.textFromNotionTextElement(properties.Name),
        queueTime: NotionClient.dateTimeFromNotionDateElement(properties.QueueTime),
        team: NotionClient.valueFromNotionSelectElement<Team>(properties.Team),
      };
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
      return {
        id: NotionClient.textFromNotionTextElement(properties.ID),
        isCap: NotionClient.boolFromNotionBooleanElement(properties.isCap),
        mmr: NotionClient.numberFromNotionNumberElement(properties.MMR),
        name: NotionClient.textFromNotionTextElement(properties.Name),
        queueTime: NotionClient.dateTimeFromNotionDateElement(properties.QueueTime),
        team: NotionClient.valueFromNotionSelectElement<Team>(properties.Team),
      };
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
    const allBallChaserPages = await this.#Client.getAll();
    const allBallChaserPageIds = allBallChaserPages.map((allBallChaserPage) => allBallChaserPage.id);

    await this.#Client.remove(allBallChaserPageIds);
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
      ID: NotionClient.notionTextElementFromText(id),
      MMR: options.mmr ? NotionClient.notionNumberElementFromNumber(options.mmr) : existingBallChaserProps.MMR,
      Name: options.name ? NotionClient.notionTextElementFromText(options.name) : existingBallChaserProps.Name,
      QueueTime: options.queueTime
        ? NotionClient.notionDateElementFromDateTime(options.queueTime)
        : existingBallChaserProps.QueueTime,
      Team: options.team ? NotionClient.notionSelectElementFromValue<Team>(options.team) : existingBallChaserProps.Team,
      isCap: options.isCap ? NotionClient.notionBooleanElementFromBool(options.isCap) : existingBallChaserProps.isCap,
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
      ID: NotionClient.notionTextElementFromText(ballChaserToAdd.id),
      MMR: NotionClient.notionNumberElementFromNumber(ballChaserToAdd.mmr),
      Name: NotionClient.notionTextElementFromText(ballChaserToAdd.name),
      QueueTime: NotionClient.notionDateElementFromDateTime(ballChaserToAdd.queueTime),
      Team: NotionClient.notionSelectElementFromValue<Team>(ballChaserToAdd.team),
      isCap: NotionClient.notionBooleanElementFromBool(ballChaserToAdd.isCap),
    };

    await this.#Client.insert(newBallChaserProperties);
  }
}

export default new QueueRepository();
