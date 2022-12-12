import React, {ChangeEvent, FormEvent} from 'react';
import {useAppDispatch, useAppSelector} from '../../app/hooks';

import deleteIcon from '../../assets/img/job-seach/delete-icon.svg';
import {setSearchLineParam} from '../../features/vacancy/vacancy-slice';
import {getResumeList} from '../../service/async-actions/async-actions-resume';

function ResumeSearchField() {
  const pageSearch = useAppSelector((state) => state.vacancy.paramsForGetVacancies.searchLine);
  const dispatch = useAppDispatch();

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    dispatch(getResumeList());
  };

  const handleEraseSearch = () => {
    dispatch(setSearchLineParam(''));
    dispatch(getResumeList());
  };

  const handleSearchVacancy = (e: ChangeEvent<HTMLInputElement>) => {
    dispatch(setSearchLineParam(e.target.value));
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
      <button type="submit" className="text-field-submit">Найти резюме</button>
    </form>
  );
}

export default ResumeSearchField;