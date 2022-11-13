const USERS = '/v1/users';

export const UsersRoutes = {
  register: USERS,
  auth: `${USERS}/authenticate`,
  refresh: `${USERS}/refresh-tokens`,
  byId: (id: number) => `${USERS}/${id}`
};
