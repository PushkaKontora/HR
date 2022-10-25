import {configureStore} from '@reduxjs/toolkit';
import exampleReducer from '../features/example/example-slice';
import generalReducer from '../features/general/general-slice';

export const store = configureStore({
  reducer: {
    example: exampleReducer,
    general: generalReducer
  },
});

export type AppDispatch = typeof store.dispatch;

export type RootState = ReturnType<typeof store.getState>;
