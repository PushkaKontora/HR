import {UserStatus} from '../types/user-status';

export const FavoriteTabs = {
  [UserStatus.user]: ['Избранные вакансии'],
  [UserStatus.employer]: ['Избранные вакансии', 'Избранные резюме'],
  [UserStatus.admin]: [],
  [UserStatus.noAuth]: []
} as const;
