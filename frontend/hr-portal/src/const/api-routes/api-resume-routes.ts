import {PRODUCT_VERSION_FOR_ROUTES} from '../../const';

const RESUME = `${PRODUCT_VERSION_FOR_ROUTES}/resumes`;

export const ResumeRoutes = {
  resume: RESUME,
  resumeByID: (id: number) => `${RESUME}/${id}`,
  publish: (id: number) => `${RESUME}/${id}/publish`,
  unpublish: (id: number) => `${RESUME}/${id}/unpublish`,
  wishlist: (sortBy: string) => `${RESUME}/wishlist?sort_by=${sortBy}`,
  modifyWishlist: (id: number) => `${RESUME}/wishlist/${id}`,
  document: (id: number) => `${RESUME}/${id}/document`
};