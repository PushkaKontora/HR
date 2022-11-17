import {createSlice} from '@reduxjs/toolkit';

import {Vacancy} from '../../types/vacancy';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';
import {Department} from '../../types/department';
import {createDepartmentShortVision} from './vacancy.actions';
import {DEFAULT_ELEMENT_DEPARTMENT, ExpectedExperienceNameString, SortingVacancyTypes} from '../../const';

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
  departments: Department[];
  departmentsShortVersions: DepartmentsShortVersions[],
  paramsForGetVacancies: {
    salaryMin: string,
    salaryMax: string,
    experience: string,
    department: string,
    searchLine: string,
    sortedItem: string,
    offset: number
  }
}

const initialState: VacancyState = {
  vacancies: {items: [], count: 0},
  vacancyByID: null,
  isOpenRespondModal: false,
  departments: [],
  departmentsShortVersions: [],
  paramsForGetVacancies: {
    salaryMin: '',
    salaryMax: '',
    experience: 'Любой',
    department: '',
    searchLine: '',
    sortedItem: SortingVacancyTypes.BY_NAME,
    offset: 1,
  }
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
      state.paramsForGetVacancies.salaryMin = action.payload;
    },
    setSalaryMax(state, action) {
      state.paramsForGetVacancies.salaryMax = action.payload;
    },
    setExperienceParam(state, action) {
      state.paramsForGetVacancies.experience = action.payload;
    },
    setDepartmentParam(state, action) {
      state.paramsForGetVacancies.department = action.payload;
    },
    setSearchLineParam(state, action) {
      state.paramsForGetVacancies.searchLine = action.payload;
    },
    setSortedItemParam(state, action) {
      state.paramsForGetVacancies.sortedItem = action.payload;
    },
    setOffsetParam(state, action) {
      state.paramsForGetVacancies.offset = action.payload;
    },
    setParamsForGetVacanciesDefault(state) {
      state.paramsForGetVacancies = initialState.paramsForGetVacancies;
    },
    setDepartments(state, action) {
      state.departments = action.payload;
      const shortVersions = createDepartmentShortVision(action.payload);
      state.departmentsShortVersions = [DEFAULT_ELEMENT_DEPARTMENT, ...shortVersions];
    }
  },
  extraReducers(builder) {
    builder
      .addCase(getVacancies.fulfilled, (state, action) => {
        state.vacancies = action.payload;
      });
  }
});

export const {
  setVacancyByID,
  setStateRespondModal,
  setSalaryMin,
  setSalaryMax,
  setSortedItemParam,
  setExperienceParam,
  setSearchLineParam,
  setDepartmentParam,
  setParamsForGetVacanciesDefault,
  setDepartments
} = vacancySlice.actions;

export default vacancySlice.reducer;