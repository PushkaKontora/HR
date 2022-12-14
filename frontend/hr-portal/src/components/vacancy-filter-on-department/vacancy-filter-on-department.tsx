import React, {useEffect, useLayoutEffect, useRef} from 'react';

import Select, {SingleValue} from 'react-select';

import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {DepartmentsShortVersions, setDepartmentParam} from '../../features/vacancy/vacancy-slice';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';
import './vacancy-filter-on-department.scss';

function VacancyFilterOnDepartment() {
  const departmentListShort = useAppSelector((state) => state.vacancy.departmentsShortVersions);
  const department = useAppSelector((state) => state.vacancy.paramsForGetVacancies.department);
  const dispatch = useAppDispatch();
  const firstUpdate = useRef(true);

  useLayoutEffect(() => {
    if (firstUpdate.current) {
      firstUpdate.current = false;
      return;
    }
  });

  useEffect(() => {
    dispatch(setDepartmentParam(department));
  }, [departmentListShort]);

  useEffect(() => {
    dispatch(getVacancies());
  }, [department]);

  const onHandlerFilterDepartment = (e: SingleValue<DepartmentsShortVersions>) => {
    dispatch(setDepartmentParam(e?.label));
  };

  return (
    <div className="filterItem filterItem__departments">
      <div className="filterItem-title">Департамент</div>
      <Select
        className="basic-single"
        classNamePrefix="select"
        name=""
        options={departmentListShort}
        value={departmentListShort.find((departmentItem) => department === departmentItem.label)}
        onChange={onHandlerFilterDepartment}
        placeholder="Выбрать департамент"
      />
    </div>
  );
}

export default VacancyFilterOnDepartment;