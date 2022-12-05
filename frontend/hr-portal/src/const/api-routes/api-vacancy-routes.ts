import {PRODUCT_VERSION_FOR_ROUTES} from '../../const';

const VACANCY = `${PRODUCT_VERSION_FOR_ROUTES}/vacancies`;

export const VacancyRoutes = {
  getVacancy: VACANCY,
  postVacancyRequest: `${PRODUCT_VERSION_FOR_ROUTES}/vacancy-requests`,
  vacancyWithID: (id: number) =>  `${VACANCY}/${id}`,
  patchStatusVacancyUnpublish: (id: number) =>  `${VACANCY}/${id}/unpublish`,
  patchStatusVacancyPublish: (id: number) =>  `${VACANCY}/${id}/publish`,
  wishlist: (sortBy: string) => `${VACANCY}/wishlist?sort_by=${sortBy}`,
  modifyWishlist: (id: number) => `${VACANCY}/wishlist/${id}`
};
