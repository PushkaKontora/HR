import {UserStatus} from '../types/user-status';
import {FavoriteTabs} from '../const/favorite-tabs';
import {User} from '../types/user';

export function getTabsByUserStatus (status: Omit<UserStatus, 'noAuth'> | undefined): readonly string[] {
  if (!status)
    return [];

  return FavoriteTabs[status as keyof typeof UserStatus];
}