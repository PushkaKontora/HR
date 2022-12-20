import {createSlice} from '@reduxjs/toolkit';

import {Vacancy} from '../../types/vacancy';
import {Department} from '../../types/department';
import {createDepartmentShortVision, getMaxPagesForPagination, makeViewDataExperience, setCompetenciesForResume, setNewParamDepartment, setNewParamExperience, setNewParamOffset, setNewParamSalaryMax, setNewParamSalaryMin, setNewParamSearchLine, setNewParamSortBy} from './vacancy.actions';
import {DEFAULT_ELEMENT_DEPARTMENT, SortingVacancyTypes, TypeActionPagination, TypeRequestVacancyModal} from '../../const';
import {addToVacancyWishlist, createVacancy, deleteFromVacancyWishlist, getVacancies, getVacanciesForEmployer, getVacancyByID, patchStatusVacancyUnpublish, postVacancyRequests, putVacancyChanges} from '../../service/async-actions/async-actions-vacancy';
import {
  getLastVacancyRequest,
} from '../../service/async-actions/async-actions-vacancy';
import {toast} from 'react-toastify';
import {getResumeList} from '../../service/async-actions/async-actions-resume';

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
    offset: number,

    competencies: string[],
  },
  maxPagesItemsForPagination: number,
  currentPage: number,
  typeActionPagination: TypeActionPagination,
  isPublishedVacancy: boolean,
  isOpenUnpublishVacancyModal: boolean;
  isOpenEditVacancyModal: boolean;
  isEditorVacancyFlag: boolean;
  editorTextVacancy: string;
  isStartRequestChangeVacancy: boolean;
  isOpenPublishVacancyModal: boolean;

  isOpenCreateVacancyModal: boolean,
  typeRequestModalVacancy: TypeRequestVacancyModal;

  isHiddenToolbar: boolean,
  prevDescriptionVacancyBYid: string

  requestDate: Date | null
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

    competencies: []
  },
  maxPagesItemsForPagination: 1,
  currentPage: 1,
  typeActionPagination: TypeActionPagination.VACANCY,
  isPublishedVacancy: true,
  isOpenUnpublishVacancyModal: false,
  isOpenEditVacancyModal: false,
  editorTextVacancy: '',
  isEditorVacancyFlag: false,
  isStartRequestChangeVacancy: false,
  isOpenPublishVacancyModal: false,

  isOpenCreateVacancyModal: false,
  typeRequestModalVacancy: TypeRequestVacancyModal.CHANGE,

  isHiddenToolbar: true,
  prevDescriptionVacancyBYid: '',

  requestDate: null
};

const vacancySlice = createSlice({
  name: 'vacancy',
  initialState,
  reducers: {
    setEditorTextVacancy(state, action) {
      if (action.payload === state.prevDescriptionVacancyBYid) {
        return;
      } else {
        state.editorTextVacancy = action.payload;
        state.isEditorVacancyFlag = false;
        state.isStartRequestChangeVacancy = true;
      }
    },
    setCompetencies(state, action) {
      state.paramsForGetVacancies.competencies = action.payload;
      setCompetenciesForResume(action.payload);
      state.paramsForGetVacancies.offset = 0;
      state.currentPage = 1;
      setNewParamOffset(0);
    },
    setTypeRequestModalVacancy(state, action) {
      state.typeRequestModalVacancy = action.payload;
    },
    setIsOpenCreateVacancyModal(state, action) {
      state.isOpenCreateVacancyModal = action.payload;
      state.isHiddenToolbar = !action.payload;
    },
    setIsOpenEditVacancyModal(state, action) {
      state.isOpenEditVacancyModal = action.payload;
      state.isHiddenToolbar = !action.payload;
    },
    setIsStartRequestChangeVacancy(state, action) {
      state.isStartRequestChangeVacancy = action.payload;
    },
    setIsEditorVacancyFlag(state, action) {
      state.isEditorVacancyFlag = action.payload;
    },
    setTypeActionPagination(state, action) {
      state.typeActionPagination = action.payload;
      state.paramsForGetVacancies.offset = 0;
      state.currentPage = 1;
      setNewParamOffset(0);
    },
    setVacancyByID(state, action) {
      state.vacancyByID = action.payload;
      state.prevDescriptionVacancyBYid = action.payload.description;
    },
    setIsPublishedVacancy(state, action) {
      state.isPublishedVacancy = action.payload;
      state.paramsForGetVacancies.offset = 0;
      state.currentPage = 1;
      setNewParamOffset(0);
    },
    setStateUnpublishedVacancy(state, action) {
      state.isOpenUnpublishVacancyModal = action.payload;
    },
    setStatePublishedVacancy(state, action) {
      state.isOpenPublishVacancyModal = action.payload;
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

      if (departmentItem && departmentItem.label !== 'Выбрать элемент') {
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
    },
    setRequestDate(state, action) {
      state.requestDate = action.payload;
    }
  },
  extraReducers(builder) {
    builder
      .addCase(getVacancies.fulfilled, (state, action) => {
        state.vacancies = action.payload;
        state.maxPagesItemsForPagination = getMaxPagesForPagination(action.payload.count);
      })
      .addCase(getVacanciesForEmployer.fulfilled, (state, action) => {
        state.vacancies = action.payload;
        state.maxPagesItemsForPagination = getMaxPagesForPagination(action.payload.count);
      })
      .addCase(patchStatusVacancyUnpublish.fulfilled, (state, action) => {
        toast.dark('Вакансия успешно снята с публикации');
      })
      .addCase(getVacancyByID.fulfilled, (state, action) => {
        state.vacancyByID = action.payload;
      })
      .addCase(getResumeList.fulfilled, (state, action) => {
        state.maxPagesItemsForPagination = getMaxPagesForPagination(action.payload.count);
      })
      .addCase(getLastVacancyRequest.fulfilled, (state, action) => {
        state.requestDate = action.payload;
      })
      .addCase(createVacancy.fulfilled, (state) => {
        toast.dark('Вы создали новую вакансию');
      })
      .addCase(putVacancyChanges.fulfilled, (state) => {
        toast.dark('Вакансия отредактирована');
      })
      .addCase(getLastVacancyRequest.rejected, (state) => {
        state.requestDate = null;
      });
  }
});

export const {
  setIsOpenCreateVacancyModal,
  setIsOpenEditVacancyModal,
  setIsStartRequestChangeVacancy,
  setStatePublishedVacancy,
  setIsEditorVacancyFlag,
  setEditorTextVacancy,
  setVacancyByID,
  setStateRespondModal,
  setStateUnpublishedVacancy,
  setSalaryMin,
  setSalaryMax,
  setSortedItemParam,
  setExperienceParam,
  setSearchLineParam,
  setDepartmentParam,
  setParamsForGetVacanciesDefault,
  setOffsetParam,
  setDepartments,
  setTypeActionPagination,
  setIsPublishedVacancy,
  setTypeRequestModalVacancy,
  setCompetencies,
  setRequestDate
} = vacancySlice.actions;

export default vacancySlice.reducer;