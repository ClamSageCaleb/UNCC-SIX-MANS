import * as faker from "faker";
import { mocked } from "ts-jest/utils";
import NotionClient from "../../helpers/NotionClient";
import NotionElementHelper from "../../helpers/NotionElementHelper";
import { BallChaserBuilder } from "../../../../.jest/Builder";
import { ActiveMatchRepository as ActiveMatchRepositoryClass } from "../ActiveMatchRepository";
import { ActiveMatchPageProperties } from "../types";
import { BallChaser, Team } from "../../../types/common";
import { Page } from "@notionhq/client/build/src/api-types";
import { PropertyValueMap } from "@notionhq/client/build/src/api-endpoints";

jest.mock("../../helpers/NotionClient");

let ActiveMatchRepository: ActiveMatchRepositoryClass;

beforeEach(async () => {
  jest.clearAllMocks();
  process.env.notion_active_match_id = faker.datatype.uuid();

  // have to wait to import the repo until after the test environment variable is set
  const ImportedRepo = await import("../ActiveMatchRepository");
  ActiveMatchRepository = ImportedRepo.default; // <- get the default export from the imported file
});

function makeMockActiveMatchPlayerPage(ballChaser: BallChaser): [Page, ActiveMatchPageProperties] {
  const mockProps: ActiveMatchPageProperties = {
    ID: NotionElementHelper.notionTextElementFromText(ballChaser.id),
    MatchID: NotionElementHelper.notionTextElementFromText(faker.datatype.uuid()),
    Reported: NotionElementHelper.notionSelectElementFromValue<Team>(null),
    Team: NotionElementHelper.notionSelectElementFromValue<Team>(ballChaser.team),
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
      database_id: process.env.notion_active_match_id ?? "",
      type: "database_id",
    },
    properties: mockProps as unknown as PropertyValueMap,
    url: "",
  };

  return [mockPage, mockProps];
}

describe("ActiveMatchRepository Tests", () => {
  it("can add an active match", async () => {
    const mockInsert = mocked(NotionClient.prototype.insert);

    const mockBallChasers = BallChaserBuilder.many(6);
    await ActiveMatchRepository.addActiveMatch(mockBallChasers);

    expect(mockInsert).toHaveBeenCalledTimes(6);
    mockBallChasers.forEach((mockBallChaser) => {
      expect(mockInsert).toHaveBeenCalledWith(
        expect.objectContaining({
          ID: NotionElementHelper.notionTextElementFromText(mockBallChaser.id),
        })
      );
    });
  });

  it("can remove all players in a match", async () => {
    const mockPlayer = BallChaserBuilder.single();
    const [mockPage, mockProps] = makeMockActiveMatchPlayerPage(mockPlayer);
    mocked(NotionClient.prototype.getById).mockResolvedValue(mockPage);

    const mockFindAllAndRemove = mocked(NotionClient.prototype.findAllAndRemove);

    await ActiveMatchRepository.removeAllPlayersInActiveMatch(mockPlayer.id);

    expect(mockFindAllAndRemove).toHaveBeenCalledTimes(1);
    expect(mockFindAllAndRemove).toHaveBeenLastCalledWith({
      filter: {
        property: "MatchID",
        text: {
          equals: NotionElementHelper.textFromNotionTextElement(mockProps.MatchID),
        },
      },
    });
  });

  it("retreives all players part of an active match", async () => {
    // FIXME
    const mockPlayers = BallChaserBuilder.many(6);

    const [mockPage, mockProps] = makeMockActiveMatchPlayerPage(mockPlayer);
    mocked(NotionClient.prototype.getAll).mockResolvedValue(mockPage);
  });
});
