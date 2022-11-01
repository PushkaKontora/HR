import {ExpectedExperience} from '../const';

export type Vacancy = {
  'id': number,
  'name': string,
  'description': string,
  'expected_experience': ExpectedExperience,
  'salary_from'?: number,
  'salary_to'?: number,
  'department': {
    'id': number,
    'name': string,
    'leader': {
      'id': number,
      'surname': string,
      'name': string,
      'patronymic': string
    }
  },
  'published_at': Date | null
}
