import {StatusCodes} from 'http-status-codes';

export const TIMEOUT_SHOW_ERROR = 3000;

export const SHOWN_STATUSES = [
  StatusCodes.BAD_REQUEST,
  StatusCodes.UNAUTHORIZED,
  StatusCodes.NOT_FOUND,
  StatusCodes.UNPROCESSABLE_ENTITY
];
