import {createAsyncThunk} from '@reduxjs/toolkit';
import {AxiosInstance} from 'axios';
import {RootState} from '../../app/store';
import {Vacancy} from '../../types/vacancy';
import {VacancyRoutes} from '../../const/api-routes/api-vacancy-routes';
import {LIMIT_ELEMENTS_ON_PAGE, SortingVacancyTypes} from '../../const';
import {Department} from '../../types/department';
import {Generics} from '../../types/generics';
import {setDepartments} from '../../features/vacancy/vacancy-slice';
import {DepartmentsRoutes} from '../../const/api-routes/api-departments-routes';

type GetVacancyParams = {
  sortBy: SortingVacancyTypes,
  offset: number
  query?: string,
  // salaryTo?: number,
  // salaryFrom?: number,
  // experience?:ExpectedExperience,
}

export const getVacancies = createAsyncThunk<{ items: Vacancy[], count: number }, GetVacancyParams, Generics>(
  'vacancy/getVacancy',
  async ({query, sortBy, offset}, {extra: api}) => {
    let strRequest = '';
    query !== undefined
      ? strRequest = `${VacancyRoutes.getVacancy}?sort_by=${sortBy}&limit=${LIMIT_ELEMENTS_ON_PAGE}&offset=${offset}${query}`
      : strRequest = `${VacancyRoutes.getVacancy}?sort_by=${sortBy}&limit=${LIMIT_ELEMENTS_ON_PAGE}&offset=${offset}`;

    const {data} = await api.get<{ items: Vacancy[], count: number }>(strRequest);
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

