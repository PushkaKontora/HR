import {PRODUCT_VERSION_FOR_ROUTES} from '../../const';

const VACANCY = `${PRODUCT_VERSION_FOR_ROUTES}/vacancies`;

export const VacancyRoutes = {
  getVacancy: VACANCY,
  postVacancyRequest: `${PRODUCT_VERSION_FOR_ROUTES}/vacancy-requests`,
  patchStatusVacancyUnpublish: (id: number) =>  `${VACANCY}/${id}/unpublish`,
};
