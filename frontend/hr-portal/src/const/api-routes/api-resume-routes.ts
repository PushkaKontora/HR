import {PRODUCT_VERSION_FOR_ROUTES} from '../../const';

const RESUME = `${PRODUCT_VERSION_FOR_ROUTES}/resumes`;

export const ResumeRoutes = {
  resume: RESUME,
  resumeByID: (id: number) => `${RESUME}/${id}`,
};