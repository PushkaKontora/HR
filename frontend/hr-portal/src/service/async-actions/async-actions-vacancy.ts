import {createAsyncThunk} from '@reduxjs/toolkit';

import {Vacancy} from '../../types/vacancy';
import {VacancyRoutes} from '../../const/api-routes/api-vacancy-routes';
import {LIMIT_ELEMENTS_ON_PAGE, SortingVacancyTypes} from '../../const';
import {Department} from '../../types/department';
import {Generics} from '../../types/generics';
import {setDepartments, setVacancyByID, VacanciesApi} from '../../features/vacancy/vacancy-slice';
import {DepartmentsRoutes} from '../../const/api-routes/api-departments-routes';
import {getParamsRequestVacancy, initialParamsVacancyRequest} from '../../features/vacancy/vacancy.actions';
import {VacancyPutChangeParams} from '../../types/vacancy-put-change-params';
import {CreateVacancyParams} from '../../types/create-vacancy-params';


export const getVacanciesForEmployer = createAsyncThunk<VacanciesApi, { isPublished: boolean, idDepartment: number, offset: number }, Generics>(
  'vacancy/getVacancyEmployer',
  async ({isPublished, idDepartment, offset}, {extra: api}) => {
    const lineUrl = `${VacancyRoutes.getVacancy}?sort_by=${SortingVacancyTypes.BY_NAME}&limit=${LIMIT_ELEMENTS_ON_PAGE}&offset=${offset}&department_id=${idDepartment}&published=${isPublished}`;
    const {data} = await api.get<VacanciesApi>(lineUrl);
    return data;
  },
);


export const VacancyWishListSortBy = {
  published_at_asc: 'published_at_asc',
  added_at_desc: 'added_at_desc'
};

export const getVacancies = createAsyncThunk<{ items: Vacancy[], count: number }, undefined, Generics>(
  'vacancy/getVacancies',
  async (arg, {extra: api}) => {

    const paramsURL = getParamsRequestVacancy();

    let lineWithNewParameters = '';

    Object.entries(paramsURL).map(([key, value]) => {
      if (key !== '&offset=' && key !== '?sort_by=' && key !== '&competencies=' && value !== initialParamsVacancyRequest[key]) {
        lineWithNewParameters += `${key}${value}`;
      }
    });

    const lineUrl = `${VacancyRoutes.getVacancy}?sort_by=${paramsURL['?sort_by=']}&published=true&limit=${LIMIT_ELEMENTS_ON_PAGE}&offset=${paramsURL['&offset=']}${lineWithNewParameters}`;
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

export const getLastVacancyRequest = createAsyncThunk<Date, number, Generics>(
  'vacancy/lastRequest',
  async (vacancyId, {dispatch, extra: api}) => {
    const {data} = await api.get(VacancyRoutes.lastVacancyRequest(vacancyId));
    return data.created_at;
  }
);

export const patchStatusVacancyUnpublish = createAsyncThunk<void, number, Generics>(
  'vacancy/setStatusVacancyUnpublish',
  async (idVacancy, {dispatch, extra: api}) => {
    await api.patch(VacancyRoutes.patchStatusVacancyUnpublish(idVacancy));
  },
);

export const patchStatusVacancyPublish = createAsyncThunk<void, number, Generics>(
  'vacancy/setStatusVacancyPublish',
  async (idVacancy, {dispatch, extra: api}) => {
    await api.patch(VacancyRoutes.patchStatusVacancyPublish(idVacancy));
  },
);

export const putVacancyChanges = createAsyncThunk<void, { idVacancy: number, data: VacancyPutChangeParams }, Generics>(
  'vacancy/putVacancyChanges',
  async ({idVacancy, data}, {dispatch, extra: api}) => {
    await api.put(VacancyRoutes.vacancyWithID(idVacancy), data);
  },
);

export const createVacancy = createAsyncThunk<void, { data: CreateVacancyParams }, Generics>(
  'vacancy/createVacancy',
  async ({data}, {dispatch, extra: api}) => {
    await api.post(VacancyRoutes.getVacancy, data);
  },
);

export const getVacancyByID = createAsyncThunk<Vacancy, number, Generics>(
  'vacancy/getVacancyByID',
  async (vacancyID, {dispatch, extra: api}) => {
    const {data} = await api.get<Vacancy>(VacancyRoutes.vacancyWithID(vacancyID));
    return data;
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
  }
);

export const deleteFromVacancyWishlist = createAsyncThunk<void, number, Generics>(
  'vacancy/deleteFromWishlist',
  async (vacancyId, {dispatch, extra: api}) => {
    await api.delete(VacancyRoutes.modifyWishlist(vacancyId));
  }
);
