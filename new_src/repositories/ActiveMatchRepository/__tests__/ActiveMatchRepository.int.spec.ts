import ActiveMatchRepository from "..";
import { BallChaserBuilder } from "../../../../.jest/Builder";

describe("Active Match Repository Integration Tests", () => {
  it("add players to active match", async () => {
    const mockBallChasers = BallChaserBuilder.many(1);
    await ActiveMatchRepository.addActiveMatch(mockBallChasers);
  });
});
