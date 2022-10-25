import {createSlice, PayloadAction} from '@reduxjs/toolkit';


interface GeneralState {
  statusUser: 'user' | 'employer' | 'admin';
}


const initialState: GeneralState = {
  statusUser: 'user',
};

const generalSlice = createSlice({
  name: 'general',
  initialState,
  reducers: {
    indicateStatus(state, action) {
      state.statusUser = action.payload;
    },
  }
});

export const {indicateStatus} = generalSlice.actions;

export default generalSlice.reducer;