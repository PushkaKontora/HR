import {configureStore} from '@reduxjs/toolkit';

import vacancyReducer from '../features/vacancy/vacancy-slice';
import generalReducer from '../features/general/general-slice';
import userReducer from '../features/user/user-slice';
import {createApi} from '../service/api';

export const api = createApi();

export const store = configureStore({
  reducer: {
    user: userReducer,
    vacancy: vacancyReducer,
    general: generalReducer
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      thunk: {
        extraArgument: api
      }
    })
});

export type AppDispatch = typeof store.dispatch;

export type RootState = ReturnType<typeof store.getState>;
