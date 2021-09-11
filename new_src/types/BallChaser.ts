import { DateTime } from "luxon";

export interface NewBallChaserFields {
  id: string;
  mmr: number;
  name: string;
  isCap?: boolean;
  team?: Team;
  queueTime?: DateTime;
}

export const enum Team {
  Blue = "Blue",
  Orange = "Orange",
}

class BallChaser {
  #id: string;
  #mmr: number;
  #name: string;
  #isCap: boolean;
  #team: Team | null;
  #queueTime: DateTime | null;

  constructor(ballChaserFields: NewBallChaserFields) {
    this.#id = ballChaserFields.id;
    this.#mmr = ballChaserFields.mmr;
    this.#name = ballChaserFields.name;
    this.#isCap = ballChaserFields.isCap ?? false;
    this.#team = ballChaserFields.team ?? null;
    this.#queueTime = ballChaserFields.queueTime ?? null;
  }

  public get id(): string {
    return this.#id;
  }

  public get mmr(): number {
    return this.#mmr;
  }

  public get name(): string {
    return this.#name;
  }

  public get isCap(): boolean {
    return this.#isCap;
  }

  public get team(): Team | null {
    return this.#team;
  }

  public get queueTime(): DateTime | null {
    return this.#queueTime;
  }
}

export default BallChaser;
