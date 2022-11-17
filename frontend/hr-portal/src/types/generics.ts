import {AppDispatch, RootState} from '../app/store';
import {AxiosInstance} from 'axios';

export type Generics = {
  dispatch: AppDispatch,
  state: RootState,
  extra: AxiosInstance
};