import {DepartmentsShortVersions} from './vacancy-slice';
import {Department} from '../../types/department';
import {ExpectedExperience, ExpectedExperienceNameString, LIMIT_ELEMENTS_ON_PAGE, SortingVacancyTypes} from '../../const';

export function createDepartmentShortVision(departmentsFull: Department[]): DepartmentsShortVersions[] {
  return departmentsFull.map(department => {
    return {'label': department.name, 'value': department.id};
  });
}

export const initialParamsVacancyRequest: { [index: string]: any } = {
  '&salary_from=': '',
  '&salary_to=': '',
  '&experience=': 'Любой',
  '&department_id=': '',
  '&search=': '',
  '?sort_by=': SortingVacancyTypes.BY_NAME,
  '&offset=': 0,
};

const paramsVacancyRequest = Object.assign({}, initialParamsVacancyRequest);

export function getParamsRequestVacancy() {
  return paramsVacancyRequest;
}

export function setNewParamSalaryMin(salaryMin: string) {
  paramsVacancyRequest['&salary_from='] = salaryMin;
}

export function setNewParamSalaryMax(salaryMax: string) {
  paramsVacancyRequest['&salary_to='] = salaryMax;
}

export function setNewParamExperience(experience: string) {
  paramsVacancyRequest['&experience='] = experience;
}

export function setNewParamDepartment(department: string) {
  paramsVacancyRequest['&department_id='] = department;
}

export function setNewParamSearchLine(searchLine: string) {
  paramsVacancyRequest['&search='] = searchLine;
}

export function setNewParamOffset(offset: number) {
  paramsVacancyRequest['&offset='] = offset;
}

export function setNewParamSortBy(sortedItem: SortingVacancyTypes) {
  paramsVacancyRequest['?sort_by='] = sortedItem as SortingVacancyTypes;
}

export function makeViewDataExperience(action: string): string {
  let valueExp = 'Любой';
  Object.entries(ExpectedExperienceNameString).map(([key, value]) => {
    if (value === action) {
      valueExp = key as ExpectedExperience;
    }
  });

  return valueExp;
}

export function getMaxPagesVacancies(countVac: number): number {
  return Math.ceil(countVac / LIMIT_ELEMENTS_ON_PAGE);
}


//todo: очищение стейта после ухода со страницы