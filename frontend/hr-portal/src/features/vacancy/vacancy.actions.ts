import {DepartmentsShortVersions} from './vacancy-slice';
import {Department} from '../../types/department';

export function createDepartmentShortVision(departmentsFull: Department[]): DepartmentsShortVersions[] {
  return departmentsFull.map(department => {
    return {'label': department.name, 'value': department.id};
  });
}