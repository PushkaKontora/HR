export const LIMIT_ELEMENTS_ON_PAGE = 10;
export const PRODUCT_VERSION_FOR_ROUTES = '/v1';

export const DEFAULT_ELEMENT_DEPARTMENT = {label: 'Выбрать элемент', value: 0};

export enum User {
  user = 'user',
  employer = 'employer',
  admin = 'admin'
}

export enum ExpectedExperience {
  NO_EXPERIENCE = 'no_experience',
  FROM_ONE_TO_THREE_YEARS = 'from_one_to_three_years',
  FROM_THREE_TO_SIX_YEARS = 'from_three_to_six_years',
  MORE_THAN_SIX_YEARS = 'more_than_six_years'
}

export const ExpectedExperienceNameString = {
  [ExpectedExperience.NO_EXPERIENCE]: 'Нет опыта',
  [ExpectedExperience.FROM_ONE_TO_THREE_YEARS]: 'От 1 года до 3 лет',
  [ExpectedExperience.FROM_THREE_TO_SIX_YEARS]: 'От 3 до 6 лет',
  [ExpectedExperience.MORE_THAN_SIX_YEARS]: 'Больше 6 лет'
};

export enum SortingVacancyTypes {
  BY_NAME = 'name_asc',
  PUBLISHED_DATE = 'published_at_desc',
  SALARY_ASC = 'salary_asc',
  SALARY_DESC = 'salary_desc'
}

export const SelectFilterCard = {
  [SortingVacancyTypes.BY_NAME]: 'По умолчанию',
  [SortingVacancyTypes.PUBLISHED_DATE]: 'По дате',
  [SortingVacancyTypes.SALARY_DESC]: 'По убыванию зарплаты',
  [SortingVacancyTypes.SALARY_ASC]: 'По возрастанию зарплаты'
};

export enum TabInHeader {
  vacancies = 'vacancies',
  resume = 'resume',
  myVacancy = 'myVacancy'
}