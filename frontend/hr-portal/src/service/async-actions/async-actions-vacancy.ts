import {createAsyncThunk} from '@reduxjs/toolkit';
import {setLoading} from '../../features/general/general-slice';

export const getVacancies = createAsyncThunk<void, number, any>(
  'vacancy/getVacancy',
  async (arg, {dispatch, extra: api}) => {
    dispatch(setLoading(true));
  }
);