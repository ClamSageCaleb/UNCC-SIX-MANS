import { Client } from "@notionhq/client";
import { DatabasesQueryParameters, InputPropertyValueMap } from "@notionhq/client/build/src/api-endpoints";
import { Page } from "@notionhq/client/build/src/api-types";

class NotionClient {
  #notionClient: Client;
  #databaseId: string;

  constructor(databaseId: string) {
    this.#notionClient = new Client({ auth: process.env.notion_token });
    this.#databaseId = databaseId;
  }

  async getById(id: string): Promise<Page | null> {
    const pages = await this.#notionClient.databases.query({
      database_id: this.#databaseId,
      filter: {
        property: "ID",
        text: {
          equals: id,
        },
      },
    });

    if (pages.results.length < 1) {
      return null;
    } else if (pages.results.length > 1) {
      throw new Error(`More than one entry with the ID: ${id}.`);
    } else {
      return pages.results[0];
    }
  }

  async getAll(args?: Omit<DatabasesQueryParameters, "database_id">): Promise<Array<Page>> {
    const response = await this.#notionClient.databases.query({ database_id: this.#databaseId, ...args });
    return response.results;
  }

  async update(pageId: string, updates: unknown): Promise<void> {
    await this.#notionClient.pages.update({
      archived: false,
      page_id: pageId,
      properties: updates as InputPropertyValueMap,
    });
  }

  async remove(pageId: string | Array<string>): Promise<void> {
    const pageIds: Array<string> = typeof pageId === "string" ? [pageId] : pageId;

    const removePromises = pageIds.map((pageId) =>
      // according to the docs archiving a page is the same as deleting it
      // https://developers.notion.com/reference/archive-delete-a-page
      this.#notionClient.pages.update({
        archived: true,
        page_id: pageId,
        properties: {},
      })
    );

    await Promise.all(removePromises);
  }

  async findAllAndRemove(args?: Omit<DatabasesQueryParameters, "database_id" | "archived">): Promise<void> {
    const allPagesToRemove = await this.getAll(args);
    const allPageIds = allPagesToRemove.map((page) => page.id);
    await this.remove(allPageIds);
  }

  async insert(newItemProps: unknown): Promise<void> {
    await this.#notionClient.pages.create({
      parent: { database_id: this.#databaseId },
      properties: newItemProps as InputPropertyValueMap,
    });
  }
}

export default NotionClient;
