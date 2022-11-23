import {createAsyncThunk} from '@reduxjs/toolkit';
import {Generics} from '../../types/generics';
import {UsersRoutes} from '../../const/api-routes/api-users-routes';
import {setLoading} from '../../features/general/general-slice';
import {HumanNameFormData} from '../../components/human-name-form/human-name-form';

export const updateEmailAction = createAsyncThunk<
  string, {id: number, email: string}, Generics>(
    'users/updateEmail',
    async (arg, {dispatch, extra: api}) => {
      const {id, ...data} = arg;
      const res = await api.patch(UsersRoutes.emailRoute(id), data);
      //dispatch(setLoading(false));
      return data.email;
    }
  );

export const resetPassword = createAsyncThunk<
  {updated_at: string}, {id: number, previous_password: string, new_password: string}, Generics>(
    'users/resetPassword',
    async (arg, {dispatch, extra: api}) => {
      const {id, ...data} = arg;
      const res = await api.patch(UsersRoutes.resetPassword(id), data);
      return res.data;
    }
  );

export const updateName = createAsyncThunk<
  HumanNameFormData, {id: number} & HumanNameFormData, Generics>(
    'users/updateName',
    async (arg, {dispatch, extra: api}) => {
      const {id, ...data} = arg;
      const res = await api.patch(UsersRoutes.updateName(id), data);
      return data;
    }
  );

export const loadUserPhoto = createAsyncThunk<
  string, {id: number, data: FormData}, Generics>(
    'users/loadUserPhoto',
    async (arg, {dispatch, extra: api}) => {
      const {id, data} = arg;
      const res = await api.post(UsersRoutes.photo(id), data);
      return res.data.photo;
    }
  );

export const deleteUserPhoto = createAsyncThunk<
  void, {id: number}, Generics>(
    'users/deletePhoto',
    async (arg, {dispatch, extra: api}) => {
      await api.delete(UsersRoutes.photo(arg.id));
    }
  );

