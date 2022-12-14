import React, {ChangeEvent, FormEvent, useLayoutEffect, useRef} from 'react';

import deleteIcon from '../../assets/img/job-seach/delete-icon.svg';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setSearchLineParam} from '../../features/vacancy/vacancy-slice';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';

function VacancySearchField() {
  const pageSearch = useAppSelector((state) => state.vacancy.paramsForGetVacancies.searchLine);
  const dispatch = useAppDispatch();
  const firstUpdate = useRef(true);

  useLayoutEffect(() => {
    if (firstUpdate.current) {
      firstUpdate.current = false;
      return;
    }
  });

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    dispatch(getVacancies());
  };

  const handleSearchVacancy = (e: ChangeEvent<HTMLInputElement>) => {
    dispatch(setSearchLineParam(e.target.value));
  };

  const handleEraseSearch = () => {
    dispatch(setSearchLineParam(''));
    dispatch(getVacancies());
  };

  return (
    <form onSubmit={handleSubmit} className="formField">
      <label className="text-field-label">
        <div className="text-field__icon">
          <input className="text-field__input" type="text" value={pageSearch} onChange={handleSearchVacancy} placeholder="Должность, профессия"/>
        </div>
        <div className="deleteIcon" onClick={handleEraseSearch}>
          <img src={deleteIcon} alt="delete icon" className="erase-icon"/>
        </div>
      </label>
      <button type="submit" className="text-field-submit">Найти вакансию</button>
    </form>
  );
}

export default VacancySearchField;