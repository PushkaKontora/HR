import bannerSearchScreen from '../../assets/img/job-seach/banner-jobSearchPage.svg';
import './job-search-screen.scss';
import VacancyList from '../../components/vacancy-list/vacancy-list';
import CardSorting from '../../components/card-sorting/card-sorting';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setDepartmentParam, setExperienceParam, setSalaryMax, setSalaryMin} from '../../features/vacancy/vacancy-slice';
import VacancySearchField from '../../components/vacancy-search-field/vacancy-search-field';
import VacancyFilterOnDepartment from '../../components/vacancy-filter-on-department/vacancy-filter-on-department';
import VacancyFilterOnExperience from '../../components/vacancy-filter-on-experience/vacancy-filter-on-experience';
import VacancyFilterOnSalary from '../../components/vacancy-filter-on-salary/vacancy-filter-on-salary';
import {useEffect} from 'react';
import {getDepartment, getVacancies} from '../../service/async-actions/async-actions-vacancy';


function JobSearchScreen() {
  const vacancies = useAppSelector((state) => state.vacancy.vacancies);
  const dispatch = useAppDispatch();

  const dataState = useAppSelector((state) => state.vacancy.paramsForGetVacancies);
  const departmentListShort = useAppSelector((state) => state.vacancy.departmentsShortVersions);


  useEffect(() => {
    dispatch(getDepartment());
  }, []);


  const handlerClearFilters = () => {
    dispatch(setExperienceParam('Любой'));
    dispatch(setSalaryMax(''));
    dispatch(setSalaryMin(''));
    dispatch(setDepartmentParam(''));
  };

  return (
    <div className="jobSearchScreen-wrapper">
      <div className="jobSearchScreen-item jobSearchScreen-item__banner">
        <img src={bannerSearchScreen} alt="banner search screen" className="bannerSearchScreen"/>
      </div>
      <div className="jobSearchScreen-item jobSearchScreen-item__searchField">
        <VacancySearchField/>
      </div>
      <div className="jobSearchScreen-item jobSearchScreen-item__content">
        <div className="contentItem contentItem__filters">
          <VacancyFilterOnDepartment/>
          <VacancyFilterOnExperience/>
          <VacancyFilterOnSalary/>
          <div className="filterItem" onClick={handlerClearFilters}>
            <div className="filterItem-title filterItem-title__clearForm">Сбросить фильтр</div>
          </div>
        </div>
        <div className="contentItem contentItem__vacancies">
          <div className="cardVacancy-title">
            <div className="title">Найдена {vacancies.count} вакансия</div>
            <CardSorting/>
          </div>
          <VacancyList/>
        </div>
      </div>
    </div>
  );
}

export default JobSearchScreen;