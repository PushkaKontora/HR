import bannerResumeScreen from '../../assets/img/resume-page/resume-page-banner.svg';
import TabStateMyVacancy from '../../components/tab-state-my-vacancy/tab-state-my-vacancy';
import PlusIcon from '../../assets/img/my-vacancy-page/plus-icon.svg';
import VacancyListEmployerMyVacancy from '../../components/vacancy-list-employer-my-vacancy/vacancy-list-employer-my-vacancy';
import './employer-resume-screen.scss';
import {useEffect} from 'react';
import {useAppDispatch} from '../../app/hooks';
import {changeActiveTabInHeader} from '../../features/page/page-slice';
import {TabInHeader} from '../../const';
import ResumeSearchField from '../../components/resume-search-field/resume-search-field';
import VacancyFilterOnDepartment from '../../components/vacancy-filter-on-department/vacancy-filter-on-department';
import VacancyFilterOnExperience from '../../components/vacancy-filter-on-experience/vacancy-filter-on-experience';
import VacancyFilterOnSalary from '../../components/vacancy-filter-on-salary/vacancy-filter-on-salary';
import CardSorting from '../../components/card-sorting/card-sorting';
import VacancyListVacanciesPage from '../../components/vacancy-list-vacancies-page/vacancy-list-vacancies-page';

function EmployerResumeScreen() {
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(changeActiveTabInHeader(TabInHeader.resume));
  }, []);

  return (
    <div className="employerResumeScree-wrapper">
      <div className="jobSearchScreen-item jobSearchScreen-item__banner">
        <img src={bannerResumeScreen} alt="banner search screen" className="bannerSearchScreen"/>
      </div>
      <div className="search-item">
        <ResumeSearchField/>
      </div>
      <div className="jobSearchScreen-item content-filters-field-wrapper">
        <div className="contentItem contentItem__filters">
          <VacancyFilterOnDepartment/>
          <VacancyFilterOnExperience/>
          <VacancyFilterOnSalary/>
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
    </div>
  );
}

export default EmployerResumeScreen;