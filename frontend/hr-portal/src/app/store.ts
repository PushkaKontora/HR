import {configureStore} from '@reduxjs/toolkit';
import exampleReducer from '../features/example/example-slice';

export const store = configureStore({
    reducer: {
        example: exampleReducer,
    },
});

export type AppDispatch = typeof store.dispatch;

export type RootState = ReturnType<typeof store.getState>;
