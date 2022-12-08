import React from 'react';
import VacancyFilterOnExperience from '../vacancy-filter-on-experience/vacancy-filter-on-experience';
import FilterOnSalary from '../filter-on-salary/filter-on-salary';

import CompetenciesField from '../competencies-field/competencies-field';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';

function ContentResumeScreen() {
  return (
    <div className="jobSearchScreen-item content-filters-field-wrapper">
      <div className="contentItem contentItem__filters">
        {/*<VacancyFilterOnDepartment/>*/}
        <VacancyFilterOnExperience/>
        <FilterOnSalary callAction={getVacancies()}/>
        <CompetenciesField/>
        {/*<div className="filterItem" onClick={handlerClearFilters}>*/}
        {/*  <div className="filterItem-title filterItem-title__clearForm">Сбросить фильтр</div>*/}
        {/*</div>*/}
      </div>
      {/*<div className="contentItem contentItem__vacancies">*/}
      {/*  <div className="cardVacancy-title">*/}
      {/*    <div className="title">Найдена {vacancies.count} вакансия</div>*/}
      {/*    <CardSorting/>*/}
      {/*  </div>*/}
      {/*  <VacancyListVacanciesPage/>*/}
      {/*</div>*/}
    </div>
  );
}

export default ContentResumeScreen;