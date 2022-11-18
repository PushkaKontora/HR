import React, {ChangeEvent, useEffect, useLayoutEffect, useRef} from 'react';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {ExpectedExperience, ExpectedExperienceNameString} from '../../const';
import {setExperienceParam} from '../../features/vacancy/vacancy-slice';

const radioInput = ['Любой'].concat(Object.values(ExpectedExperienceNameString));

function VacancyFilterOnExperience() {
  const experience = useAppSelector((state) => state.vacancy.paramsForGetVacancies.experience);
  const dispatch = useAppDispatch();
  const firstUpdate = useRef(true);

  useLayoutEffect(() => {
    if (firstUpdate.current) {
      firstUpdate.current = false;
      return;
    }
  });

  useEffect(() => {
    dispatch(getVacancies());
  }, [experience]);

  const onHandlerClickRadio = (el: ChangeEvent<HTMLInputElement>) => {
    dispatch(setExperienceParam(el.target.value));
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