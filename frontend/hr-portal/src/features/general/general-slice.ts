import {createSlice} from '@reduxjs/toolkit';
import {User} from '../../types/user';


interface GeneralState {
  statusUser: User;
}


const initialState: GeneralState = {
  statusUser: User.noAuth,
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