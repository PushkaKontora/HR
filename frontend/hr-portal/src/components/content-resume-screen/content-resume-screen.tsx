import React from 'react';
import VacancyFilterOnExperience from '../vacancy-filter-on-experience/vacancy-filter-on-experience';
import FilterOnSalary from '../filter-on-salary/filter-on-salary';

import CompetenciesField from '../competencies-field/competencies-field';
import ResumeScreenResumeList from '../resume-screen-resume-list/resume-screen-resume-list';
import {getResumeList} from '../../service/async-actions/async-actions-resume';
import {setCompetencies, setExperienceParam, setSalaryMax, setSalaryMin} from '../../features/vacancy/vacancy-slice';
import {useAppDispatch} from '../../app/hooks';

function ContentResumeScreen() {
  const dispatch = useAppDispatch();

  const handlerClearFilters = () => {
    dispatch(setExperienceParam('Любой'));
    dispatch(setSalaryMax(''));
    dispatch(setSalaryMin(''));
    dispatch(setCompetencies([]));
  };

  return (
    <div className="jobSearchScreen-item content-filters-field-wrapper">
      <div className="contentItem contentItem__filters">
        {/*<VacancyFilterOnDepartment/>*/}
        <VacancyFilterOnExperience/>
        <FilterOnSalary callAction={getResumeList()}/>
        <CompetenciesField/>
        <div className="filterItem" onClick={handlerClearFilters}>
          <div className="filterItem-title filterItem-title__clearForm">Сбросить фильтр</div>
        </div>
      </div>
      <ResumeScreenResumeList/>
    </div>
  );
}

export default ContentResumeScreen;