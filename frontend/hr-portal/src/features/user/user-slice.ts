import {createSlice} from '@reduxjs/toolkit';
import {ResumeUser} from '../../types/resume';
import {TabInHeader} from '../../const';

interface UserState {
  resumeUser: ResumeUser | null;
  activeTabInHeader: TabInHeader | null;
}


const initialState: UserState = {
  resumeUser: null,
  activeTabInHeader: TabInHeader.vacancies
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setResumeUser(state, action) {
      state.resumeUser = action.payload;
    },
    changeActiveTabInHeader(state, action) {
      state.activeTabInHeader = action.payload;
    }
  }
});

export const {
  setResumeUser,
  changeActiveTabInHeader
} = userSlice.actions;

export default userSlice.reducer;