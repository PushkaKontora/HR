import {PRODUCT_VERSION_FOR_ROUTES} from '../../const';

const USERS = `${PRODUCT_VERSION_FOR_ROUTES}/users`;

export const UsersRoutes = {
  register: USERS,
  auth: `${USERS}/authenticate`,
  refresh: `${USERS}/refresh-tokens`,
  byId: (id: number) => `${USERS}/${id}`,
  resetPassword: (id: number) => `${USERS}/${id}/reset-password`
};