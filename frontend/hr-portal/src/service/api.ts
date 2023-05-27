import axios, {AxiosError, InternalAxiosRequestConfig, AxiosResponse} from 'axios';
import {getToken} from './token-manager';
import {SHOWN_STATUSES} from '../const/errors';
import {processErrorHandle} from './error-handle';
import {StatusCodes} from 'http-status-codes';
import {ServerError, StandartError, UnprocessableEntityError} from '../types/error-types';
import {store} from '../app/store';
import {setLoading} from '../features/general/general-slice';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
const TIMEOUT = 5000;

export const createApi = () => {
  const api = axios.create(
    {
      baseURL: BACKEND_URL,
      timeout: TIMEOUT
    }
  );

  api.interceptors.request.use(
    (config: InternalAxiosRequestConfig<any>) => {
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
      store.dispatch(setLoading(false));
      if (error.response && SHOWN_STATUSES.includes(error.response.status)) {
        if (error.response.status === StatusCodes.UNPROCESSABLE_ENTITY) {
          const data = error.response.data as UnprocessableEntityError;
          processErrorHandle(data.error.msg);
          throw error;
        } else {
          const data = error.response.data as StandartError;
          processErrorHandle(data.msg);
          throw error;
        }
      }
    }
  );

  return api;
};