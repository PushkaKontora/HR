import {DepartmentsShortVersions} from './vacancy-slice';
import {Department} from '../../types/department';
import {DEFAULT_ELEMENT_DEPARTMENT, ExpectedExperienceNameString, LIMIT_ELEMENTS_ON_PAGE, SortingVacancyTypes, TypesFilters} from '../../const';
import {useAppSelector} from '../../app/hooks';
import {VacancyRequestParams} from '../../types/vacancy-request-params';

export function createDepartmentShortVision(departmentsFull: Department[]): DepartmentsShortVersions[] {
  return departmentsFull.map(department => {
    return {'label': department.name, 'value': department.id};
  });
}


type GetVacancyWithNewParams = {
  typeFilters: TypesFilters,
  data?: string
}

export function getVacancyWithNewParams(params: any): string {
  const {paramsForGetVacancies, departmentList} = params;

  let lineWithNewParameters = '';

  if (paramsForGetVacancies.salaryMin !== '') {
    lineWithNewParameters += `&salary_from=${paramsForGetVacancies.salaryMin}`;

  }
  if (paramsForGetVacancies.salaryMax !== '') {
    lineWithNewParameters += `&salary_to=${paramsForGetVacancies.salaryMax}`;
  }
  if (paramsForGetVacancies.experience !== 'Любой') {
    const experienceData = Object.entries(ExpectedExperienceNameString).filter(e => e[1] === paramsForGetVacancies.experience);
    lineWithNewParameters += `&experience=${experienceData[0][0]}`;
  }
  if (paramsForGetVacancies.department !== (DEFAULT_ELEMENT_DEPARTMENT.label || '')) {
    const elementWithLabel = departmentList.find((el: DepartmentsShortVersions) => el.label === paramsForGetVacancies.department);
    if (elementWithLabel) {
      lineWithNewParameters += `&department_id=${elementWithLabel.value}`;
    }
  }
  if (paramsForGetVacancies.searchLine !== '') {
    lineWithNewParameters += `&search=${paramsForGetVacancies.searchLine}`;
  }


  return `${lineWithNewParameters}`;
  //dispatch(getVacancies({sortBy: SortingVacancyTypes.BY_NAME, offset: 1, query: lineWithNewParameters}));
}