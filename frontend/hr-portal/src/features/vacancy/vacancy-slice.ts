import {createSlice} from '@reduxjs/toolkit';

import {Vacancy} from '../../types/vacancy';
import {Department} from '../../types/department';
import {createDepartmentShortVision, getMaxPagesVacancies, makeViewDataExperience, setNewParamDepartment, setNewParamExperience, setNewParamOffset, setNewParamSalaryMax, setNewParamSalaryMin, setNewParamSearchLine, setNewParamSortBy} from './vacancy.actions';
import {DEFAULT_ELEMENT_DEPARTMENT, SortingVacancyTypes} from '../../const';
import {getVacancies, getVacanciesForEmployer} from '../../service/async-actions/async-actions-vacancy';

export type VacanciesApi = {
  items: Vacancy[],
  count: number
}

export type DepartmentsShortVersions = {
  'value': number;
  'label': string
}

interface VacancyState {
  vacancies: VacanciesApi;
  vacanciesForEmployer: Vacancy[];
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
  },
  maxPagesVacancies: number,
  currentPage: number,
  isGetVacanciesEmployer: boolean,
  isPublishedVacancy: boolean
}

const initialState: VacancyState = {
  vacancies: {items: [], count: 0},
  vacanciesForEmployer: [],
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
    offset: 0,
  },
  maxPagesVacancies: 1,
  currentPage: 1,
  isGetVacanciesEmployer: false,
  isPublishedVacancy: true
};

const vacancySlice = createSlice({
  name: 'vacancy',
  initialState,
  reducers: {
    setIsGetVacanciesEmployer(state, action) {
      state.isGetVacanciesEmployer = action.payload;
    },
    setVacancyByID(state, action) {
      state.vacancyByID = action.payload;
    },
    setIsPublishedVacancy(state, action) {
      state.isPublishedVacancy = action.payload;
    },
    setStateRespondModal(state, action) {
      state.isOpenRespondModal = action.payload;
    },
    setSalaryMin(state, action) {
      state.paramsForGetVacancies.salaryMin = action.payload;
      setNewParamSalaryMin(action.payload.toString());
      state.paramsForGetVacancies.offset = 0;
      state.currentPage = 1;
      setNewParamOffset(0);
    },
    setSalaryMax(state, action) {
      state.paramsForGetVacancies.salaryMax = action.payload;
      setNewParamSalaryMax(action.payload.toString());
      state.paramsForGetVacancies.offset = 0;
      state.currentPage = 1;
      setNewParamOffset(0);
    },
    setExperienceParam(state, action) {
      state.paramsForGetVacancies.experience = action.payload;
      const valueExp = makeViewDataExperience(action.payload);
      setNewParamExperience(valueExp);
      state.paramsForGetVacancies.offset = 0;
      state.currentPage = 1;
      setNewParamOffset(0);
    },
    setDepartmentParam(state, action) {
      state.paramsForGetVacancies.department = action.payload;
      const departmentItem = state.departmentsShortVersions.find((departmentItem) => action.payload === departmentItem.label);

      if (departmentItem) {
        setNewParamDepartment(departmentItem.value.toString());
      } else {
        setNewParamDepartment('');
      }

      state.paramsForGetVacancies.offset = 0;
      state.currentPage = 1;
      setNewParamOffset(0);
    },
    setSearchLineParam(state, action) {
      state.paramsForGetVacancies.searchLine = action.payload;
      setNewParamSearchLine(action.payload);
      state.paramsForGetVacancies.offset = 0;
      state.currentPage = 1;
      setNewParamOffset(0);
    },
    setSortedItemParam(state, action) {
      state.paramsForGetVacancies.sortedItem = action.payload;
      setNewParamSortBy(action.payload as SortingVacancyTypes);
      state.paramsForGetVacancies.offset = 0;
      state.currentPage = 1;
      setNewParamOffset(0);
    },
    setOffsetParam(state, action) {
      state.paramsForGetVacancies.offset = action.payload - 1;
      state.currentPage = action.payload;
      setNewParamOffset(action.payload - 1);
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
        state.maxPagesVacancies = getMaxPagesVacancies(action.payload.count);
      })
      .addCase(getVacanciesForEmployer.fulfilled, (state, action) => {
        state.vacancies = action.payload;
        state.maxPagesVacancies = getMaxPagesVacancies(action.payload.count);
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
  setOffsetParam,
  setDepartments,
  setIsGetVacanciesEmployer,
  setIsPublishedVacancy
} = vacancySlice.actions;

export default vacancySlice.reducer;