import axios, {AxiosRequestConfig, AxiosResponse} from 'axios';
import {getToken} from './token-manager';

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

  return api;
};