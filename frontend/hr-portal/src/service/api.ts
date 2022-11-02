import axios, {AxiosError, AxiosRequestConfig, AxiosResponse} from 'axios';
import {getToken} from './token-manager';
import {SHOWN_STATUSES} from '../const/errors';
import {processErrorHandle} from './error-handle';
import {StatusCodes} from 'http-status-codes';
import {ServerError, StandartError, UnprocessableEntityError} from '../types/error-types';

const BACKEND_URL = 'http://127.0.0.1:8000';
const TIMEOUT = 5000;

export const createApi = () => {
  const api = axios.create(
    {
      baseURL: BACKEND_URL,
      timeout: TIMEOUT
    }
  );

  api.interceptors.request.use(
    (config: AxiosRequestConfig) => {
      const token = getToken();

      if (token) {
        config.headers = config.headers ?? {};
        config.headers.Authorization = `Bearer ${token}`;
      }

      return config;
    }
  );

  api.interceptors.response.use(
    (res:AxiosResponse) => res,
    (error: AxiosError<ServerError>) => {
      if (error.response && error.response.status in SHOWN_STATUSES) {
        if (error.response.status === StatusCodes.UNPROCESSABLE_ENTITY) {
          const data = error.response.data as UnprocessableEntityError;
          processErrorHandle(data.error.msg);
        } else {
          const data = error.response.data as StandartError;
          processErrorHandle(data.msg);
        }
      }
    }
  );

  return api;
};