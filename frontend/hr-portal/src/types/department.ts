import {Leader} from './leader';

export type Department = {
  'id': number;
  'name': string;
  'description': string;
  'vacancies_amount': number;
  'leader': Leader
}