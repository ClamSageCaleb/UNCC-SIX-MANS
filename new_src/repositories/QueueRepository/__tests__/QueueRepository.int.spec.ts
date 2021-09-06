/* eslint-disable @typescript-eslint/no-non-null-assertion */
import BallChaser, { NewBallChaserFields } from "../../../types/BallChaser";
import * as faker from "faker";
import { DateTime } from "luxon";
import QueueRepository from "..";

function verifyBallChasersAreEqual(expectedBallChaser: BallChaser, actualBallChaser: BallChaser): void {
  expect(actualBallChaser).not.toBeNull();
  expect(actualBallChaser!.id).toBe(expectedBallChaser.id);
  expect(actualBallChaser!.mmr).toBe(expectedBallChaser.mmr);
  expect(actualBallChaser!.name).toBe(expectedBallChaser.name);
  expect(actualBallChaser!.queueTime!.toISO()).toBe(expectedBallChaser.queueTime!.toISO());
  expect(actualBallChaser!.team).toBe(expectedBallChaser.team);
  expect(actualBallChaser!.isCap).toBe(expectedBallChaser.isCap);
}

describe("Queue Repository Integration Tests", () => {
  it("add and remove BallChaser from queue", async () => {
    const ballChaserToAdd = new BallChaser({
      id: faker.random.word(),
      isCap: false,
      mmr: faker.datatype.number(),
      name: faker.random.word(),
      queueTime: DateTime.now().set({ millisecond: 0, second: 0 }),
      team: undefined,
    });

    await QueueRepository.addBallChaserToQueue(ballChaserToAdd);
    const retrievedBallChaser = await QueueRepository.getBallChaserInQueue(ballChaserToAdd.id);

    verifyBallChasersAreEqual(ballChaserToAdd, retrievedBallChaser!);

    await QueueRepository.removeBallChaserFromQueue(ballChaserToAdd.id);
    const retrievedBallChaserShouldBeNull = await QueueRepository.getBallChaserInQueue(ballChaserToAdd.id);
    expect(retrievedBallChaserShouldBeNull).toBeNull();
  });

  it("gets and removes everyone from the queue", async () => {
    const ballChaserToAdd1 = new BallChaser({
      id: faker.random.word(),
      isCap: false,
      mmr: faker.datatype.number(),
      name: faker.random.word(),
      queueTime: DateTime.now().set({ millisecond: 0, second: 0 }),
      team: undefined,
    });
    const ballChaserToAdd2 = new BallChaser({
      id: faker.random.word(),
      isCap: false,
      mmr: faker.datatype.number(),
      name: faker.random.word(),
      queueTime: DateTime.now().set({ millisecond: 0, second: 0 }),
      team: undefined,
    });

    const addOne = QueueRepository.addBallChaserToQueue(ballChaserToAdd1);
    const addTwo = QueueRepository.addBallChaserToQueue(ballChaserToAdd2);
    await Promise.all([addOne, addTwo]);

    const allBallChasers = await QueueRepository.getAllBallChasersInQueue();
    expect(allBallChasers).toHaveLength(2);

    await QueueRepository.removeAllBallChasersFromQueue();
    const shouldBeEmptyBallChasers = await QueueRepository.getAllBallChasersInQueue();
    expect(shouldBeEmptyBallChasers).toHaveLength(0);
  });

  it("can update a BallChaser", async () => {
    const fields: NewBallChaserFields = {
      id: faker.random.word(),
      isCap: false,
      mmr: faker.datatype.number(),
      name: faker.random.word(),
      queueTime: DateTime.now().set({ millisecond: 0, second: 0 }),
      team: undefined,
    };

    const ballChaserToAdd = new BallChaser(fields);
    await QueueRepository.addBallChaserToQueue(ballChaserToAdd);

    const newName = faker.random.word();
    const expectedUpdatedBallChaser = new BallChaser({
      ...fields,
      name: newName,
    });
    await QueueRepository.updateBallChaserInQueue({
      id: ballChaserToAdd.id,
      name: newName,
    });

    const updatedBallChaser = await QueueRepository.getBallChaserInQueue(ballChaserToAdd.id);
    verifyBallChasersAreEqual(expectedUpdatedBallChaser, updatedBallChaser!);

    await QueueRepository.removeBallChaserFromQueue(ballChaserToAdd.id);
    const retrievedBallChaserShouldBeNull = await QueueRepository.getBallChaserInQueue(ballChaserToAdd.id);
    expect(retrievedBallChaserShouldBeNull).toBeNull();
  });
});
