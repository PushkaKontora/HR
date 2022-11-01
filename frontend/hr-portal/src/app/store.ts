import {configureStore, getDefaultMiddleware} from '@reduxjs/toolkit';
import exampleReducer from '../features/example/example-slice';
import generalReducer from '../features/general/general-slice';
import {createApi} from '../service/api';

export const api = createApi();

export const store = configureStore({
  reducer: {
    example: exampleReducer,
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
