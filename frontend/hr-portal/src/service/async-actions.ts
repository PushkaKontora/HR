import {createAsyncThunk} from '@reduxjs/toolkit';
import {indicateStatus, reset, setError, setLoading, setUser} from '../features/general/general-slice';
import {AppDispatch, RootState, store} from '../app/store';
import {AxiosInstance} from 'axios';
import {decodeToken, dropToken, getToken, saveToken} from './token-manager';
import {UsersRoutes} from '../const/api-users-routes';
import {useSelector} from 'react-redux';
import {useAppSelector} from '../app/hooks';
import {User} from '../types/user';
import {TIMEOUT_SHOW_ERROR} from '../const/errors';

type Generics = {
  dispatch: AppDispatch,
  state: RootState,
  extra: AxiosInstance
};

// get any user action here

export const getAuthUser = createAsyncThunk<void, number, Generics>(
  'users/getUser',
  async (arg, {dispatch, extra: api}) => {
    dispatch(setLoading(true));
    const res = await api.get(UsersRoutes.byId(arg));
    const user: User = res.data;

    dispatch(setUser(user));

    dispatch(setLoading(false));
  }
);

// register function here

export const login = createAsyncThunk<void, {email: string, password: string}, Generics>(
  'users/login',
  async (arg, {dispatch, extra: api}) => {
    dispatch(setLoading(true));
    const res = await api.post(UsersRoutes.auth, arg);

    saveToken(res.data.access_token);
    const userPermission = decodeToken()?.permission;
    dispatch(indicateStatus(userPermission));

    dispatch(setLoading(false));
  });

export const logout = createAsyncThunk<void, undefined, Generics>(
  'users/logout',
  async (_arg, {dispatch, extra: api}) => {
    dispatch(setLoading(true));
    dropToken();
    // drop refresh token from cookie
    dispatch(reset());
    dispatch(setLoading(false));
  },
);

export const clearErrorAction = createAsyncThunk(
  'game/clearError',
  () => {
    setTimeout(
      () => store.dispatch(setError(null)),
      TIMEOUT_SHOW_ERROR,
    );
  },
);
