import {UserStatus} from '../types/user-status';

export const StringStatuses = {
  [UserStatus.noAuth]: 'не авторизован',
  [UserStatus.user]: 'сотрудник',
  [UserStatus.employer]: 'руководитель',
  [UserStatus.admin]: 'администратор'
};
