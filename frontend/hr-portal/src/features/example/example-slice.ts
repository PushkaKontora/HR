import {createSlice, PayloadAction} from '@reduxjs/toolkit';

interface ExampleState {
  valueCount: number;
}

const initialState: ExampleState = {
  valueCount: 0,
};

const exampleSlice = createSlice({
  name: 'example',
  initialState,
  reducers: {
    incremented(state) {
      state.valueCount++
    },
    expl(state, action: PayloadAction<number>) {
      state.valueCount += action.payload
      // action.payload - то, что мы можем получить, если положем что-то в функцию в компоненте,
      //   state - внутреннее хранилище
    },
  }
});

export const {incremented, expl} = exampleSlice.actions;

export default exampleSlice.reducer;