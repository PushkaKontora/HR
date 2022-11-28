import {createSlice} from '@reduxjs/toolkit';
import {ResumeUser} from '../../types/resume';
import {TabInHeader} from '../../const';

interface UserState {
  resumeUser: ResumeUser | null;
}


const initialState: UserState = {
  resumeUser: null,
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setResumeUser(state, action) {
      state.resumeUser = action.payload;
    }
  }
});

export const {
  setResumeUser,
} = userSlice.actions;

export default userSlice.reducer;