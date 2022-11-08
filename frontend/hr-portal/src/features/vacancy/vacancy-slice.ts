import {createSlice} from '@reduxjs/toolkit';
import {Vacancy} from '../../types/vacancy';

interface VacancyState {
  vacancyByID: Vacancy | null;
}

const initialState: VacancyState = {
  vacancyByID: null
};

const vacancySlice = createSlice({
  name: 'vacancy',
  initialState,
  reducers: {
    setVacancyByID(state, action) {
      state.vacancyByID = action.payload;
    },
  }
});

export const {setVacancyByID} = vacancySlice.actions;

export default vacancySlice.reducer;