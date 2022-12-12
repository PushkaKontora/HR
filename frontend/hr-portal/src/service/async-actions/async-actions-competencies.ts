import {createAsyncThunk} from '@reduxjs/toolkit';
import {Generics} from '../../types/generics';
import {CompetenciesRoutes} from '../../const/api-routes/api-competencies-routes';
import {Competency} from '../../types/competency';

export const getCompetenciesAction = createAsyncThunk<Array<Competency>, undefined, Generics>(
  'competencies/all',
  async (_arg, {extra: api}) => {
    const result = await api.get(CompetenciesRoutes.all);
    return result.data;
  }
);