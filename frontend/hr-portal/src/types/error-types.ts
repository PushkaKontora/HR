export type ServerError = StandartError | UnprocessableEntityError;

export type StandartError = {
  msg: string
};

export type UnprocessableEntityError = {
  error: {
    code: number,
    msg: string
  }
};
