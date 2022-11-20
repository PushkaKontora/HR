import {createAsyncThunk} from '@reduxjs/toolkit';
import {indicateStatus, reset, setError, setLoading, setUser} from '../../features/general/general-slice';
import {AppDispatch, RootState, store} from '../../app/store';
import {AxiosInstance, AxiosResponse} from 'axios';
import {decodeToken, dropToken, getToken, saveToken} from '../token-manager';
import {UsersRoutes} from '../../const/api-routes/api-users-routes';
import {User} from '../../types/user';
import {TIMEOUT_SHOW_ERROR} from '../../const/errors';
import {SignInData} from '../../types/sign-in-data';
import {StatusCodes} from 'http-status-codes';
import {Generics} from '../../types/generics';
import {useAppSelector} from '../../app/hooks';
import {ResumeRoutes} from '../../const/api-routes/api-resume-routes';
import {setResumeUser} from '../../features/user/user-slice';
import {ResumeUser} from '../../types/resume';

// get any user action here

export const getAuthUser = createAsyncThunk<void, number, Generics>(
  'users/getUser',
  async (arg, {dispatch, extra: api}) => {
    dispatch(setLoading(true));
    const res = await api.get(UsersRoutes.byId(arg));
    const user: User = res.data;

    if (user) {
      dispatch(getResumeUser(user));
    }
    dispatch(setUser(user));

    dispatch(setLoading(false));
  }
);

export const signIn = createAsyncThunk<void, SignInData, Generics>(
  'users/signin',
  async (arg, {dispatch, extra: api}) => {
    dispatch(setLoading(true));
    const res = await api.post(UsersRoutes.register, arg);

    if (res.status === StatusCodes.OK) {
      dispatch(login({email: arg.email, password: arg.password}));
    } else {
      dispatch(setLoading(false));
    }
  }
);

export const login = createAsyncThunk<void, { email: string, password: string }, Generics>(
  'users/login',
  async (arg, {dispatch, extra: api}) => {
    dispatch(setLoading(true));
    const res = await api.post(UsersRoutes.auth, arg);

    saveToken(res.data.access_token);
    const userPermission = decodeToken()?.permission;
    dispatch(indicateStatus(userPermission));

    dispatch(setLoading(false));
  });

export const resetPassword = createAsyncThunk<Promise<AxiosResponse>, { id: number, previous_password: string, new_password: string }, Generics>(
  'users/resetPassword',
  async (arg, {dispatch, extra: api}) => {
    dispatch(setLoading(true));

    const res = api.patch(UsersRoutes.resetPassword(arg.id));
    dispatch(setLoading(false));

    return res;
  }
);

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


export const getResumeUser = createAsyncThunk<void, User, Generics>(
  'user/getResumeUser',
  async (user, {dispatch, extra: api}) => {
    if (user.resume.id) {
      const resume = await api.get(ResumeRoutes.resumeByID(user.resume.id));
      dispatch(setResumeUser(resume.data));
    }
  }
);
