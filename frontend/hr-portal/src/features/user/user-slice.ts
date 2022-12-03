import {createSlice} from '@reduxjs/toolkit';
import {ResumeUser} from '../../types/resume';
import {TabInHeader} from '../../const';
import {deleteUserPhoto, loadUserPhoto, resetPassword, updateEmailAction, updateName} from '../../service/async-actions/async-actions-profile';
import {getCompetenciesAction} from '../../service/async-actions/async-actions-competencies';
import {deleteUser} from '../../service/async-actions/async-actions-delete-user';
import {UserStatus} from '../../types/user-status';
import {logout} from '../../service/async-actions/async-actions-user';
import browserHistory from '../../service/browser-history';

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