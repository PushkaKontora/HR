import {createSlice} from '@reduxjs/toolkit';

import {ResumeUser} from '../../types/resume';
import {getResumeWishlist} from '../../service/async-actions/async-actions-resume';
import {Vacancy} from '../../types/vacancy';
import {getVacancyWishlist} from '../../service/async-actions/async-actions-vacancy';

interface UserState {
  resumeUser: ResumeUser | null;
  favoriteVacancies: Vacancy[],
  favoriteResumes: ResumeUser[]
}


const initialState: UserState = {
  resumeUser: null,
  favoriteVacancies: [],
  favoriteResumes: []
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setResumeUser(state, action) {
      state.resumeUser = action.payload;
    }
  },
  extraReducers(builder) {
    builder
      .addCase(getVacancyWishlist.fulfilled, (state, action) => {
        state.favoriteVacancies = action.payload;
      })
      .addCase(getResumeWishlist.fulfilled, (state, action) => {
        state.favoriteResumes = action.payload;
      });
  }
});

export const {
  setResumeUser,
} = userSlice.actions;

export default userSlice.reducer;