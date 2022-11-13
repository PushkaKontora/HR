import {User} from '../types/user';
import {StringStatuses} from '../const/statuses';
import {UserStatus} from '../types/user-status';

export function getFullName(user: User | null) {
  const f = (s: string | null | undefined) => s ? s : '';
  return `${f(user?.name)} ${f(user?.surname)} ${f(user?.patronymic)}`;
}

export function userStatusToString(user: User | null) {
  return StringStatuses[<UserStatus>user?.permission];
}

export function getDate(utc: string | undefined) {
  if (!utc) {
    return 'нет данных';
  }

  const date = new Date(utc);
  return date.toLocaleDateString();
}
