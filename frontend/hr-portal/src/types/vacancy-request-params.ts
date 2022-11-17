import {SortingVacancyTypes, TypesFilters} from '../const';

export type VacancyRequestParams = {
  sortBy: SortingVacancyTypes,
  offset: number
  typeFilters: TypesFilters,
  data: string | null
}