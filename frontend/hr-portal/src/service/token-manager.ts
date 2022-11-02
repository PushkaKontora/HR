import {AccessTokenPayload} from '../types/token_payload';
import jwtDecode, {InvalidTokenError} from 'jwt-decode';
import {Exception} from 'sass';
import {redirect} from 'react-router-dom';
import {processErrorHandle} from './error-handle';
import {useAppDispatch} from '../app/hooks';
import {getAuthUser} from './async-actions';
import {AppDispatch} from '../app/store';
import {indicateStatus} from '../features/general/general-slice';

const AUTH_TOKEN_KEY_NAME = 'auth_token';

export type Token = string;

export const getToken = (): Token => {
  const token = localStorage.getItem(AUTH_TOKEN_KEY_NAME);
  return token ?? '';
};

export const saveToken = (token: Token): void => {
  localStorage.setItem(AUTH_TOKEN_KEY_NAME, token);
};

export const dropToken = (): void => {
  localStorage.removeItem(AUTH_TOKEN_KEY_NAME);
};

export const decodeToken = (): AccessTokenPayload | undefined => {
  const token = getToken();

  if (!token) {
    return undefined;
  }

  return jwtDecode(token);
};

export const checkToken = (dispatch: AppDispatch) => {
  const token = decodeToken();

  if (token !== undefined) {
    const id = token.user_id;
    const permission = token.permission;
    dispatch(indicateStatus(permission));
    dispatch(getAuthUser(id));
  }
};
