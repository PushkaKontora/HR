import {createSlice} from '@reduxjs/toolkit';

import {Vacancy} from '../../types/vacancy';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';
import {Department} from '../../types/department';
import {createDepartmentShortVision} from './vacancy.actions';

type VacanciesApi = {
  items: Vacancy[],
  count: number
}

export type DepartmentsShortVersions = {
  'value': number;
  'label': string
}

interface VacancyState {
  vacancies: VacanciesApi;
  vacancyByID: Vacancy | null;
  isOpenRespondModal: boolean;
  salaryMin: string,
  salaryMax: string,
  departments: Department[];
  departmentsShortVersions: DepartmentsShortVersions[]
}

const initialState: VacancyState = {
  vacancies: {items: [], count: 0},
  vacancyByID: null,
  isOpenRespondModal: false,
  salaryMin: '',
  salaryMax: '',
  departments: [],
  departmentsShortVersions: [],
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
    },
    setDepartments(state, action) {
      state.departments = action.payload;
      state.departmentsShortVersions = createDepartmentShortVision(action.payload);
    }
  },
  extraReducers(builder) {
    builder
      .addCase(getVacancies.fulfilled, (state, action) => {
        state.vacancies = action.payload;
      });
  }
});

export const {setVacancyByID, setStateRespondModal, setSalaryMin, setSalaryMax, setDepartments} = vacancySlice.actions;

export default vacancySlice.reducer;