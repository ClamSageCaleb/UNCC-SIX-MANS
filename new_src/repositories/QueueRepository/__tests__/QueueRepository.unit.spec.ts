/* eslint-disable @typescript-eslint/no-non-null-assertion */
import * as faker from "faker";
import { mocked } from "ts-jest/utils";
import { BallChaserPageProperties, UpdateBallChaserOptions } from "../types";
import NotionClient from "../../helpers/NotionClient";
import { DateTime } from "luxon";
import { PropertyValueMap } from "@notionhq/client/build/src/api-endpoints";
import BallChaser from "../../../types/BallChaser";
import { Page } from "@notionhq/client/build/src/api-types";
import { QueueRepository as QueueRepositoryClass } from "../QueueRepository";

jest.mock("../helpers/NotionClient");

interface MockBallChaserResponse {
  mockBallChaser: BallChaser;
  mockBallChaserPageProperties: BallChaserPageProperties;
  mockPage: Page;
}

function getMockBallChaser(): MockBallChaserResponse {
  const mockBallChaser = new BallChaser({
    id: faker.random.word(),
    isCap: false,
    mmr: faker.datatype.number(),
    name: faker.random.word(),
    queueTime: DateTime.fromJSDate(faker.date.future()).set({ millisecond: 0, second: 0 }),
    team: undefined,
  });

  const mockBallChaserPageProperties: BallChaserPageProperties = {
    ID: {
      rich_text: [{ text: { content: mockBallChaser.id }, type: "text" }],
    },
    MMR: {
      number: mockBallChaser.mmr,
    },
    Name: {
      rich_text: [{ text: { content: mockBallChaser.name }, type: "text" }],
    },
    QueueTime: {
      date: { start: mockBallChaser.queueTime!.toUTC().toISO() },
    },
    Team: { select: null },
    isCap: { checkbox: mockBallChaser.isCap },
  };

  const mockPage: Page = {
    archived: false,
    cover: null,
    created_time: "",
    icon: null,
    id: faker.datatype.uuid(),
    last_edited_time: "",
    object: "page",
    parent: {
      database_id: process.env.notion_queue_id ?? "",
      type: "database_id",
    },
    properties: mockBallChaserPageProperties as unknown as PropertyValueMap,
    url: "",
  };

  return {
    mockBallChaser,
    mockBallChaserPageProperties,
    mockPage,
  };
}

function verifyBallChasersAreEqual(expectedBallChaser: BallChaser, actualBallChaser: BallChaser): void {
  expect(actualBallChaser).not.toBeNull();
  expect(actualBallChaser!.id).toBe(expectedBallChaser.id);
  expect(actualBallChaser!.mmr).toBe(expectedBallChaser.mmr);
  expect(actualBallChaser!.name).toBe(expectedBallChaser.name);
  expect(actualBallChaser!.queueTime!.toISO()).toBe(expectedBallChaser.queueTime!.toISO());
  expect(actualBallChaser!.team).toBe(expectedBallChaser.team);
  expect(actualBallChaser!.isCap).toBe(expectedBallChaser.isCap);
}

let QueueRepository: QueueRepositoryClass;

beforeEach(async () => {
  jest.clearAllMocks();
  process.env.notion_queue_id = faker.datatype.uuid();

  // have to wait to import the repo until after the test environment variable is set
  const ImportedRepo = await import("../QueueRepository");
  QueueRepository = ImportedRepo.default; // <- get the default export from the imported file
});

describe("Queue Repository tests", () => {
  it("gets BallChaser using ID when BallChaser exists", async () => {
    const { mockBallChaser: expectedBallChaser, mockPage } = getMockBallChaser();
    mocked(NotionClient.prototype.getById).mockResolvedValue(mockPage);

    const actualBallChaser = await QueueRepository.getBallChaserInQueue(expectedBallChaser.id);

    verifyBallChasersAreEqual(expectedBallChaser, actualBallChaser!);
  });

  it("returns null when BallChaser does not exist with ID", async () => {
    mocked(NotionClient.prototype.getById).mockResolvedValue(null);

    const actualBallChaser = await QueueRepository.getBallChaserInQueue(faker.datatype.uuid());
    expect(actualBallChaser).toBeNull();
  });

  it("retrieves all BallChasers in queue", async () => {
    const { mockBallChaser: expectedBallChaser1, mockPage: mockPage1 } = getMockBallChaser();
    const { mockBallChaser: expectedBallChaser2, mockPage: mockPage2 } = getMockBallChaser();

    mocked(NotionClient.prototype.getAll).mockResolvedValue([mockPage1, mockPage2]);

    const actualBallChasers = await QueueRepository.getAllBallChasersInQueue();

    expect(actualBallChasers).toHaveLength(2);
    verifyBallChasersAreEqual(expectedBallChaser1, actualBallChasers[0]);
    verifyBallChasersAreEqual(expectedBallChaser2, actualBallChasers[1]);
  });

  it("removes BallChaser when found in queue", async () => {
    const { mockBallChaser, mockPage } = getMockBallChaser();
    mocked(NotionClient.prototype.getById).mockResolvedValue(mockPage);
    const mockRemove = mocked(NotionClient.prototype.remove);

    await expect(QueueRepository.removeBallChaserFromQueue(mockBallChaser.id)).resolves.not.toThrowError();
    expect(mockRemove).toHaveBeenCalledTimes(1);
  });

  it("throws error when trying to remove BallChaser when not found in queue", async () => {
    mocked(NotionClient.prototype.getById).mockResolvedValue(null);

    await expect(QueueRepository.removeBallChaserFromQueue(faker.datatype.uuid())).rejects.toThrowError();
  });

  it("removes all BallChasers in queue", async () => {
    const { mockPage: mockPage1 } = getMockBallChaser();
    const { mockPage: mockPage2 } = getMockBallChaser();

    const mockRemove = mocked(NotionClient.prototype.remove);
    mocked(NotionClient.prototype.getAll).mockResolvedValue([mockPage1, mockPage2]);

    await expect(QueueRepository.removeAllBallChasersFromQueue()).resolves.not.toThrowError();
    expect(mockRemove).toHaveBeenCalledTimes(1);
    expect(mockRemove).toHaveBeenLastCalledWith(expect.arrayContaining([mockPage1.id, mockPage2.id]));
  });

  it("updates BallChaser when BallChaser is found", async () => {
    const { mockBallChaser, mockPage } = getMockBallChaser();
    const { mockBallChaser: updatedBallChaser, mockBallChaserPageProperties: updateProperties } = getMockBallChaser();
    mocked(NotionClient.prototype.getById).mockResolvedValue(mockPage);
    const mockUpdate = mocked(NotionClient.prototype.update);

    const updateOptions: UpdateBallChaserOptions = {
      id: mockBallChaser.id,
      isCap: updatedBallChaser.isCap,
      mmr: updatedBallChaser.mmr,
      name: updatedBallChaser.name,
      queueTime: updatedBallChaser.queueTime,
      team: updatedBallChaser.team,
    };

    // overwrite random id with the one we need for matching
    updateProperties.ID.rich_text[0].text.content = mockBallChaser.id;

    await QueueRepository.updateBallChaserInQueue(updateOptions);
    expect(mockUpdate).toHaveBeenCalledTimes(1);
    expect(mockUpdate).toHaveBeenLastCalledWith(mockPage.id, updateProperties);
  });

  it("throws when player to update is not found", async () => {
    const { mockBallChaser } = getMockBallChaser();
    mocked(NotionClient.prototype.getById).mockResolvedValue(null);
    const mockUpdate = mocked(NotionClient.prototype.update);

    await expect(QueueRepository.updateBallChaserInQueue(mockBallChaser)).rejects.toThrowError();
    expect(mockUpdate).not.toHaveBeenCalled();
  });

  it("adds BallChaser to queue", async () => {
    mocked(NotionClient.prototype.getById).mockResolvedValue(null);
    const { mockBallChaser, mockBallChaserPageProperties } = getMockBallChaser();
    const mockInsert = mocked(NotionClient.prototype.insert);

    await QueueRepository.addBallChaserToQueue(mockBallChaser);
    expect(mockInsert).toHaveBeenCalledTimes(1);
    expect(mockInsert).toHaveBeenLastCalledWith(mockBallChaserPageProperties);
  });

  it("throws when BallChaser already exists", async () => {
    const { mockBallChaser, mockPage } = getMockBallChaser();
    mocked(NotionClient.prototype.getById).mockResolvedValue(mockPage);
    const mockInsert = mocked(NotionClient.prototype.insert);

    await expect(QueueRepository.addBallChaserToQueue(mockBallChaser)).rejects.toThrowError();
    expect(mockInsert).not.toHaveBeenCalled();
  });
});
