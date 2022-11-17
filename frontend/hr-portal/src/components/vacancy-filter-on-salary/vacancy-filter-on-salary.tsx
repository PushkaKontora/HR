import React, {ChangeEvent, useEffect} from 'react';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setSalaryMax, setSalaryMin} from '../../features/vacancy/vacancy-slice';
import {timeoutCollection} from 'time-events-manager/src/timeout/timeout-decorator';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';

function VacancyFilterOnSalary() {
  const salaryMax = useAppSelector((state) => state.vacancy.paramsForGetVacancies.salaryMax);
  const salaryMin = useAppSelector((state) => state.vacancy.paramsForGetVacancies.salaryMin);
  const dispatch = useAppDispatch();

  const dataState = useAppSelector((state) => state.vacancy.paramsForGetVacancies);
  const departmentListShort = useAppSelector((state) => state.vacancy.departmentsShortVersions);



  useEffect(() => {
    timeoutCollection.removeAll();
    setTimeout(() =>  dispatch(getVacancies({dataState, departmentListShort})), 800);
  }, [salaryMin, salaryMax]);

  const handleChangeMinSalary = (e: ChangeEvent<HTMLInputElement>) => {
    dispatch(setSalaryMin(e.target.value));
  };

  const handleChangeMaxSalary = (e: ChangeEvent<HTMLInputElement>) => {
    dispatch(setSalaryMax(e.target.value));
  };
  
  return (
    <div className="filterItem filterItem__salary">
      <div className="filterItem-title">Зарплата</div>
      <div className="salaryInput-wrapper">
        <div className="text-field-salary text-field-salary__min">
          <input className="text-field-salary-input" type="number" min="0" value={salaryMin} onChange={handleChangeMinSalary} placeholder="min"/>
        </div>
        <div className="text-field-salary text-field-salary__max">
          <input className="text-field-salary-input" type="number" min="0" value={salaryMax} onChange={handleChangeMaxSalary} placeholder="max"/>
        </div>
      </div>
    </div>
  );
}

export default VacancyFilterOnSalary;