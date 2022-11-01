import {UserStatus} from './user-status';

export type User = {
  id: number;
  email: string;
  permission: Omit<UserStatus, 'noAuth'>;
  surname: string;
  name: string;
  patronymic: string;
  photo: string;
  resume: {id: number};
  department: {id: number};
  password: {updated_at: string};
};
