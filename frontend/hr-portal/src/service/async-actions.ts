import {createAsyncThunk} from '@reduxjs/toolkit';
import {indicateStatus, reset, setLoading, setUser} from '../features/general/general-slice';
import {AppDispatch, RootState, store} from '../app/store';
import {AxiosInstance} from 'axios';
import {dropToken, saveToken} from './token-manager';
import {UsersRoutes} from '../const/api-users-routes';
import {useSelector} from 'react-redux';
import {useAppSelector} from '../app/hooks';

type AccessToken = {
  access_token: string;
}

type Generics = {
  dispatch: AppDispatch,
  state: RootState,
  extra: AxiosInstance
};

export const getUser = createAsyncThunk<void, number, Generics>(
  'users/getUser',
  async (arg, {dispatch, extra: api}) => {
    dispatch(setLoading(true));
    const user = await api.get(UsersRoutes.byId(arg));
    dispatch(setUser(user));

    const status = useAppSelector((state) => state.general.statusUser);
    dispatch(indicateStatus(status));
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
