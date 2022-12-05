import {createAsyncThunk} from '@reduxjs/toolkit';

import {Vacancy} from '../../types/vacancy';
import {VacancyRoutes} from '../../const/api-routes/api-vacancy-routes';
import {LIMIT_ELEMENTS_ON_PAGE, SortingVacancyTypes} from '../../const';
import {Department} from '../../types/department';
import {Generics} from '../../types/generics';
import {setDepartments} from '../../features/vacancy/vacancy-slice';
import {DepartmentsRoutes} from '../../const/api-routes/api-departments-routes';
import {getParamsRequestVacancy, initialParamsVacancyRequest} from '../../features/vacancy/vacancy.actions';

type GetVacancyParams = {
  sortBy: SortingVacancyTypes,
  offset: number
  query?: string,
}

export const VacancyWishListSortBy = {
  published_at_asc: 'published_at_asc',
  added_at_desc: 'added_at_desc'
};

export const getVacancies = createAsyncThunk<{ items: Vacancy[], count: number }, undefined, Generics>(
  'vacancy/getVacancy',
  async (arg, {extra: api}) => {

    const paramsURL = getParamsRequestVacancy();

    let lineWithNewParameters = '';

    Object.entries(paramsURL).map(([key, value]) => {
      if (key !== '&offset=' && key !== '?sort_by=' && value !== initialParamsVacancyRequest[key]) {
        lineWithNewParameters += `${key}${value}`;
      }
    });
    // const {dataState, departmentListShort} = arg;
    // let lineWithNewParameters = '';

    // if (dataState.salaryMin !== '') {
    //   lineWithNewParameters += `&salary_from=${dataState.salaryMin}`;
    // }
    // if (dataState.salaryMax !== '') {
    //   lineWithNewParameters += `&salary_to=${dataState.salaryMax}`;
    // }
    // if (dataState.experience !== 'Любой') {
    //   const experienceData = Object.entries(ExpectedExperienceNameString).filter(e => e[1] === dataState.experience);
    //   lineWithNewParameters += `&experience=${experienceData[0][0]}`;
    // }
    // if (dataState.department !== (DEFAULT_ELEMENT_DEPARTMENT.label || '')) {
    //   const elementWithLabel = departmentListShort.find((el: DepartmentsShortVersions) => el.label === dataState.department);
    //   if (elementWithLabel) {
    //     lineWithNewParameters += `&department_id=${elementWithLabel.value}`;
    //   }
    // }
    // if (dataState.searchLine !== '') {
    //   lineWithNewParameters += `&search=${dataState.searchLine}`;
    // }

    const lineUrl = `${VacancyRoutes.getVacancy}?sort_by=${paramsURL['?sort_by=']}&limit=${LIMIT_ELEMENTS_ON_PAGE}&offset=${paramsURL['&offset=']}${lineWithNewParameters}`;
    console.log(lineUrl);
    const {data} = await api.get<{ items: Vacancy[], count: number }>(lineUrl);
    return data;
  },
);

export const getDepartment = createAsyncThunk<void, undefined, Generics>(
  'vacancy/getDepartment',
  async (_arg, {dispatch, extra: api}) => {
    const {data} = await api.get<Department[]>(DepartmentsRoutes.getDepartments);
    dispatch(setDepartments(data));
  },
);

export const postVacancyRequests = createAsyncThunk<void, FormData, Generics>(
  'vacancy/postVacancyRequests',
  async (data, {dispatch, extra: api}) => {
    await api.post(VacancyRoutes.postVacancyRequest, data);
  },
);

export const getVacancyWishlist = createAsyncThunk<Vacancy[], string, Generics>(
  'vacancy/wishlist',
  async (arg, {dispatch, extra: api}) => {
    const res = await api.get(VacancyRoutes.wishlist(arg));
    return res.data;
  }
);

export const addToVacancyWishlist = createAsyncThunk<void, number, Generics>(
  'vacancy/addToWishlist',
  async (vacancyId, {dispatch, extra: api}) => {
    await api.post(VacancyRoutes.modifyWishlist(vacancyId));
    await getVacancyWishlist(VacancyWishListSortBy.added_at_desc);
  }
);

export const deleteFromVacancyWishlist = createAsyncThunk<void, number, Generics>(
  'vacancy/deleteFromWishlist',
  async (vacancyId, {dispatch, extra: api}) => {
    await api.delete(VacancyRoutes.modifyWishlist(vacancyId));
    await getVacancyWishlist(VacancyWishListSortBy.added_at_desc);
  }
);
