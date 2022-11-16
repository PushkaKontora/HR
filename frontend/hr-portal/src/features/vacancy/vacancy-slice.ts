import {createSlice} from '@reduxjs/toolkit';
import {Vacancy} from '../../types/vacancy';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';

type VacanciesApi = {
  items: Vacancy[],
  count: number
}

interface VacancyState {
  vacancies: VacanciesApi;
  vacancyByID: Vacancy | null;
  isOpenRespondModal: boolean;
  salaryMin: string,
  salaryMax: string,
}

const initialState: VacancyState = {
  vacancies: {items: [], count: 0},
  vacancyByID: null,
  isOpenRespondModal: false,
  salaryMin: '',
  salaryMax: '',
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
    },
    setSalaryMin(state, action) {
      state.salaryMin = action.payload;
    },
    setSalaryMax(state, action) {
      state.salaryMax = action.payload;
    }
  },
  extraReducers(builder) {
    builder
      .addCase(getVacancies.fulfilled, (state, action) => {
        state.vacancies = action.payload;
      });
  }
});

export const {setVacancyByID, setStateRespondModal, setSalaryMin, setSalaryMax} = vacancySlice.actions;

export default vacancySlice.reducer;