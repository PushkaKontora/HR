import VacancySearchField from '../vacancy-search-field/vacancy-search-field';
import VacancyFilterOnDepartment from '../vacancy-filter-on-department/vacancy-filter-on-department';
import VacancyFilterOnExperience from '../vacancy-filter-on-experience/vacancy-filter-on-experience';
import VacancyFilterOnSalary from '../vacancy-filter-on-salary/vacancy-filter-on-salary';
import CardSorting from '../card-sorting/card-sorting';
import VacancyListVacanciesPage from '../vacancy-list-vacancies-page/vacancy-list-vacancies-page';
import {setDepartmentParam, setExperienceParam, setSalaryMax, setSalaryMin} from '../../features/vacancy/vacancy-slice';
import {useAppDispatch, useAppSelector} from '../../app/hooks';

function VacancyContent() {
  const vacancies = useAppSelector((state) => state.vacancy.vacancies);
  const dispatch = useAppDispatch();

  const handlerClearFilters = () => {
    dispatch(setExperienceParam('Любой'));
    dispatch(setSalaryMax(''));
    dispatch(setSalaryMin(''));
    dispatch(setDepartmentParam(''));
  };

  return (
    <>
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
          <VacancyListVacanciesPage/>
        </div>
      </div>
    </>
  );
}

export default VacancyContent;