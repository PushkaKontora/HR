import {createAsyncThunk} from '@reduxjs/toolkit';
import {Generics} from '../../types/generics';
import {UsersRoutes} from '../../const/api-routes/api-users-routes';

export const deleteUser = createAsyncThunk<void, {id: number}, Generics>(
  'users/delete',
  async (arg, {dispatch, extra: api}) => {
    await api.delete(UsersRoutes.byId(arg.id));
  }
);