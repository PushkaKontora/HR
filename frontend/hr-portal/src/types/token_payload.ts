import {UserStatus} from './user-status';

export type AccessTokenPayload = {
  type: string,
  user_id: number,
  permission: Omit<UserStatus, 'noAuth'>,
  expires_in: number
};
