import {VacancyPutChangeParams} from './vacancy-put-change-params';

export interface CreateVacancyParams extends VacancyPutChangeParams {
  department_id: number,
}