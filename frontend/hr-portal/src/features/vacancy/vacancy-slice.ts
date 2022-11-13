import {createSlice} from '@reduxjs/toolkit';
import {Vacancy} from '../../types/vacancy';

interface VacancyState {
  vacancyByID: Vacancy | null;
  isOpenRespondModal: boolean;
}

const initialState: VacancyState = {
  vacancyByID: null,
  isOpenRespondModal: false
};

const vacancySlice = createSlice({
  name: 'vacancy',
  initialState,
  reducers: {
    setVacancyByID(state, action) {
      state.vacancyByID = action.payload;
    },
    setStateRespondModal(state, action) {
      state.isOpenRespondModal = action.payload;
    }
  }
});

export const {setVacancyByID, setStateRespondModal} = vacancySlice.actions;

export default vacancySlice.reducer;