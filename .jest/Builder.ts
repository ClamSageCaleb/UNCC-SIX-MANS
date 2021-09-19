import { BallChaser, Team } from "../new_src/types/common";
import * as faker from "faker";
import { DateTime } from "luxon";
import { Page } from "@notionhq/client/build/src/api-types";
import { ActiveMatchPageProperties } from "../new_src/repositories/ActiveMatchRepository/types";
import NotionElementHelper from "../new_src/repositories/helpers/NotionElementHelper";

abstract class Builder<T> {
  abstract isEqual(a: T, b: T): boolean;

  abstract single(overrides?: Partial<T>): T;

  many(count: number, overrides?: Partial<T>): Array<T> {
    const items: Array<T> = [];

    for (let i = 0; i < count; i++) {
      let isNotUnique = true;
      let hardStopCounter = 0;
      let item: T;

      do {
        if (hardStopCounter === 1000) {
          throw new Error(
            "Generated too many items without finding a unique instance. You may need to adjust your isEqual implementation."
          );
        }

        hardStopCounter++;
        item = this.single(overrides);
        isNotUnique = items.some((i) => this.isEqual(item, i));
      } while (isNotUnique);

      items.push(item);
    }

    return items;
  }
}

class BallChaserBuilderClass extends Builder<BallChaser> {
  isEqual(a: BallChaser, b: BallChaser) {
    return a.id === b.id;
  }

  single(overrides?: Partial<BallChaser>) {
    return {
      id: faker.datatype.uuid(),
      isCap: faker.datatype.boolean(),
      mmr: faker.datatype.number(),
      name: faker.random.word(),
      queueTime: DateTime.fromJSDate(faker.date.future()).set({ millisecond: 0, second: 0 }),
      team: faker.random.arrayElement([Team.Blue, Team.Orange]),
      ...overrides,
    };
  }
}
export const BallChaserBuilder = new BallChaserBuilderClass();

class ActiveMatchPagePropsBuilderClass extends Builder<ActiveMatchPageProperties> {
  isEqual(a: ActiveMatchPageProperties, b: ActiveMatchPageProperties) {
    return a.MatchID === b.MatchID && a.ID === b.ID;
  }

  single(overrides?: Partial<ActiveMatchPageProperties>) {
    const mockBallChaser = BallChaserBuilder.single();

    return {
      ID: NotionElementHelper.notionTextElementFromText(mockBallChaser.id),
      MatchID: NotionElementHelper.notionTextElementFromText(faker.datatype.uuid()),
      Reported: NotionElementHelper.notionSelectElementFromValue<Team>(
        faker.random.arrayElement([Team.Blue, Team.Orange])
      ),
      Team: NotionElementHelper.notionSelectElementFromValue<Team>(mockBallChaser.team),
      ...overrides,
    };
  }
}
export const ActiveMatchPagePropsBuilder = new ActiveMatchPagePropsBuilderClass();

class PageBuilderClass extends Builder<Page> {
  isEqual(a: Page, b: Page) {
    return a.id === b.id;
  }

  single(overrides?: Partial<Page>) {
    return {
      archived: false,
      cover: null,
      created_time: "",
      icon: null,
      id: faker.datatype.uuid(),
      last_edited_time: "",
      object: "page",
      parent: {
        database_id: "",
        type: "database_id",
      },
      properties: {},
      url: "",
      ...overrides,
    } as Page;
  }
}
export const PageBuilder = new PageBuilderClass();
