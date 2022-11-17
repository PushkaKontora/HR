import React, {ChangeEvent, useEffect} from 'react';
import {getDepartment, getVacancies} from '../../service/async-actions/async-actions-vacancy';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {ExpectedExperienceNameString} from '../../const';
import {setExperienceParam} from '../../features/vacancy/vacancy-slice';
import {timeoutCollection} from 'time-events-manager/src/timeout/timeout-decorator';

const radioInput = ['Любой'].concat(Object.values(ExpectedExperienceNameString));

function VacancyFilterOnExperience() {
  const experience = useAppSelector((state) => state.vacancy.paramsForGetVacancies.experience);
  const dispatch = useAppDispatch();

  const dataState = useAppSelector((state) => state.vacancy.paramsForGetVacancies);
  const departmentListShort = useAppSelector((state) => state.vacancy.departmentsShortVersions);

  useEffect(() => {
    dispatch(getVacancies({dataState, departmentListShort}));
  }, [experience]);


  const onHandlerClickRadio = (e: ChangeEvent<HTMLInputElement>) => {
    dispatch(setExperienceParam(e.target.value));
  };

  return (
    <div className="filterItem">
      <div className="filterItem-title">Требуемый стаж работы</div>
      {
        radioInput.map((value, index) => (
          <div key={index} className="radio-wrapper">
            <input
              className="radioInput"
              type="radio"
              name="site_name"
              id={index.toString()}
              value={value}
              checked={experience === value}
              onChange={onHandlerClickRadio}
            />
            <label htmlFor={index.toString()}>{value}</label>
          </div>
        ))
      }
    </div>
  );
}

export default VacancyFilterOnExperience;