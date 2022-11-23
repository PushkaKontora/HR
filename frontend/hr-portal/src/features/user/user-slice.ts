import {createSlice, isPending} from '@reduxjs/toolkit';
import {ResumeUser} from '../../types/resume';
import {createResumeAction} from '../../service/async-actions/async-actions-resume';

interface UserState {
  resumeUser: ResumeUser | null;
}


const initialState: UserState = {
  resumeUser: null
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

export const {setResumeUser} = userSlice.actions;

export default userSlice.reducer;