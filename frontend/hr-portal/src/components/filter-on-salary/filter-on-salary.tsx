import React, {ChangeEvent, useEffect, useLayoutEffect, useRef} from 'react';
import {AsyncThunkAction} from '@reduxjs/toolkit';

import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setSalaryMax, setSalaryMin} from '../../features/vacancy/vacancy-slice';
import {timeoutCollection} from 'time-events-manager/src/timeout/timeout-decorator';
import {Vacancy} from '../../types/vacancy';
import {Generics} from '../../types/generics';

type FilterOnSalaryProps = {
  salaryMax?: string,
  salaryMin?: string,
  callAction: AsyncThunkAction<{ items: Vacancy[]; count: number; }, undefined, Generics>
};

function FilterOnSalary(props: FilterOnSalaryProps) {
  const {callAction} = props;
  const salaryMax = useAppSelector((state) => state.vacancy.paramsForGetVacancies.salaryMax);
  const salaryMin = useAppSelector((state) => state.vacancy.paramsForGetVacancies.salaryMin);
  const dispatch = useAppDispatch();
  const firstUpdate = useRef(true);

  useLayoutEffect(() => {
    if (firstUpdate.current) {
      firstUpdate.current = false;
      return;
    }
  });

  useEffect(() => {
    timeoutCollection.removeAll();
    setTimeout(() => dispatch(callAction), 800);
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

export default FilterOnSalary;