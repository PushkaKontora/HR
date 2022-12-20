import {UserStatus} from '../types/user-status';
import {FavoriteTabs} from '../const/favorite-tabs';

export function getTabsByUserStatus (status: Omit<UserStatus, 'noAuth'> | undefined): readonly string[] {
  if (!status)
    return [];

  return FavoriteTabs[status as keyof typeof UserStatus];
}

export function isFavorite<T extends {id: number}>(obj: T, favorites: T[]) {
  return favorites
    .map((value) => value.id)
    .includes(obj.id);
}
