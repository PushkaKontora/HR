import React, {ChangeEvent, FormEvent, useEffect} from 'react';
import deleteIcon from '../../assets/img/job-seach/delete-icon.svg';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setSearchLineParam} from '../../features/vacancy/vacancy-slice';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';

function VacancySearchField() {
  const pageSearch = useAppSelector((state) => state.vacancy.paramsForGetVacancies.searchLine);
  const dataState = useAppSelector((state) => state.vacancy.paramsForGetVacancies);
  const departmentListShort = useAppSelector((state) => state.vacancy.departmentsShortVersions);

  const dispatch = useAppDispatch();


  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    dispatch(getVacancies({dataState, departmentListShort}));
  };

  const handleSearchVacancy = (e: ChangeEvent<HTMLInputElement>) => {
    dispatch(setSearchLineParam(e.target.value));
  };

  const handleEraseSearch = () => {
    dispatch(setSearchLineParam(''));
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
      <button type="submit" className="text-field-submit">Найти&nbsp;вакансию</button>
    </form>
  );
}

export default VacancySearchField;