import {createAsyncThunk} from '@reduxjs/toolkit';

import {indicateStatus, reset, setError, setLoading, setUser} from '../../features/general/general-slice';
import {store} from '../../app/store';
import {decodeToken, dropToken, saveToken} from '../token-manager';
import {UsersRoutes} from '../../const/api-routes/api-users-routes';
import {User} from '../../types/user';
import {TIMEOUT_SHOW_ERROR} from '../../const/errors';
import {SignInData} from '../../types/sign-in-data';
import {StatusCodes} from 'http-status-codes';
import {Generics} from '../../types/generics';
import {ResumeRoutes} from '../../const/api-routes/api-resume-routes';
import {setResumeUser} from '../../features/user/user-slice';
import browserHistory from '../browser-history';
import {UserStatus} from '../../types/user-status';
import {TabInHeader} from '../../const';
import {changeActiveTabInHeader} from '../../features/page/page-slice';

export const getAuthUser = createAsyncThunk<void, number, Generics>(
  'users/getUser',
  async (arg, {dispatch, extra: api}) => {
    dispatch(setLoading(true));
    const res = await api.get(UsersRoutes.byId(arg))
      .then((u) => {
        if (u.data.permission === UserStatus.user) {
          dispatch(getResumeUser(u.data));
        }
        if (u.data.permission === UserStatus.employer) {
          dispatch(changeActiveTabInHeader(TabInHeader.myVacancy));
        }
        return u;
      });
    const user: User = res.data;

    dispatch(setUser(user));

    dispatch(setLoading(false));
  }
);

export const signUp = createAsyncThunk<void, SignInData, Generics>(
  'users/signup',
  async (arg, {dispatch, extra: api}) => {
    dispatch(setLoading(true));
    const res = await api.post(UsersRoutes.register, arg);

    if (res.status === StatusCodes.OK) {
      dispatch(login({email: arg.email, password: arg.password}));
      browserHistory.push('/');
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

export const logout = createAsyncThunk<void, undefined, Generics>(
  'users/logout',
  async (_arg, {dispatch, extra: api}) => {
    dispatch(setLoading(true));
    dropToken();
    //browserHistory.go(-2);
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

export const getResumeById = createAsyncThunk<void, number, Generics>(
  'user/getResumeUser',
  async (id, {dispatch, extra: api}) => {
    const resume = await api.get(ResumeRoutes.resumeByID(id));
    dispatch(setResumeUser(resume.data));
  }
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