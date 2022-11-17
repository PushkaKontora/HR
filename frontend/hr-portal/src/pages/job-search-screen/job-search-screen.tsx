import React, {ChangeEvent, FormEvent, useCallback, useEffect, useRef, useState} from 'react';
import bannerSearchScreen from '../../assets/img/job-seach/banner-jobSearchPage.svg';
import deleteIcon from '../../assets/img/job-seach/delete-icon.svg';
import './job-search-screen.scss';
import VacancyList from '../../components/vacancy-list/vacancy-list';
import CardSorting from '../../components/card-sorting/card-sorting';
import Select, {SingleValue} from 'react-select';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setSalaryMax, setSalaryMin} from '../../features/vacancy/vacancy-slice';
import {getDepartment, getVacancies} from '../../service/async-actions/async-actions-vacancy';
import {ExpectedExperienceNameString, SortingVacancyTypes} from '../../const';
import {timeoutCollection} from 'time-events-manager/src/timeout/timeout-decorator';

const radioInput = ['Любой'].concat(Object.values(ExpectedExperienceNameString));


type DepartmentsShortVersions = {
  'value': number;
  'label': string
}

const initialStateJobScreen = {
  radioChecked: radioInput[0],
  salaryMin: '',
  salaryMax: '',
  selectDepartment: null
};

const defaultElement = {label: 'Выбрать элемент', value: 0};

function JobSearchScreen() {
  const [pageSearch, setPageSearch] = useState('');
  const [radioChecked, setRadioChecked] = useState(initialStateJobScreen.radioChecked);
  const [selectDepartment, setSelectDepartment] = useState<null | string | undefined>(initialStateJobScreen.selectDepartment);
  const [departmentList, setDepartmentList] = useState<DepartmentsShortVersions[]>([]);
  const salaryMin = useAppSelector((state) => state.vacancy.salaryMin);
  const salaryMax = useAppSelector((state) => state.vacancy.salaryMax);
  const vacancies = useAppSelector((state) => state.vacancy.vacancies);
  const departments = useAppSelector((state) => state.vacancy.departmentsShortVersions);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(getDepartment());
  }, []);
  useEffect(() => {
    setDepartmentList([defaultElement, ...departments]);
  }, [departments]);

  useEffect(() => {
    timeoutCollection.removeAll();
    setTimeout(() => getVacancyWithNewParams(), 1000);
  }, [salaryMin, salaryMax]);

  useEffect(() => {
    getVacancyWithNewParams();
    console.log(selectDepartment);
  }, [radioChecked, selectDepartment]);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setPageSearch(e.target.value);
  };

  const handleChangeMinSalary = (e: ChangeEvent<HTMLInputElement>) => {
    dispatch(setSalaryMin(e.target.value));
  };

  const handleChangeMaxSalary = (e: ChangeEvent<HTMLInputElement>) => {
    dispatch(setSalaryMax(e.target.value));
  };

  const handleEraseSearch = () => {
    setPageSearch('');
  };

  const onHandlerClickRadio = (e: ChangeEvent<HTMLInputElement>) => {
    setRadioChecked(e.target.value);
  };

  const onHandlerFilterDepartment = (e: SingleValue<DepartmentsShortVersions>) => {
    setSelectDepartment(e?.label);
  };

  const getVacancyWithNewParams = () => {
    let lineWithNewParameters = '';
    if (salaryMin !== '') {
      lineWithNewParameters += `&salary_from=${salaryMin.toString()}`;
    }
    if (salaryMax !== '') {
      lineWithNewParameters += `&salary_to=${salaryMax.toString()}`;
    }
    if (radioChecked !== radioInput[0]) {
      const experienceData = Object.entries(ExpectedExperienceNameString).filter(e => e[1] === radioChecked);
      lineWithNewParameters += `&experience=${experienceData[0][0]}`;
    }
    if (selectDepartment !== defaultElement.label) {
      const elementWithLabel = departmentList.find((el) => el.label === selectDepartment);
      if (elementWithLabel) {
        lineWithNewParameters += `&department_id=${elementWithLabel.value}`;
      }
    }

    dispatch(getVacancies({sortBy: SortingVacancyTypes.BY_NAME, offset: 1, query: lineWithNewParameters}));
    console.log(lineWithNewParameters);
  };

  const handlerClearFilters = () => {
    setRadioChecked(initialStateJobScreen.radioChecked);
    dispatch(setSalaryMax(initialStateJobScreen.salaryMax));
    dispatch(setSalaryMin(initialStateJobScreen.salaryMin));
    setSelectDepartment(initialStateJobScreen.selectDepartment);
  };

  return (
    <div className="jobSearchScreen-wrapper">
      <div className="jobSearchScreen-item jobSearchScreen-item__banner">
        <img src={bannerSearchScreen} alt="banner search screen" className="bannerSearchScreen"/>
      </div>
      <div className="jobSearchScreen-item jobSearchScreen-item__searchField">
        <form onSubmit={handleSubmit} className="formField">
          <label className="text-field-label">
            <div className="text-field__icon">
              <input className="text-field__input" type="text" value={pageSearch} onChange={handleChange} placeholder="Должность, профессия"/>
            </div>
            <div className="deleteIcon" onClick={handleEraseSearch}>
              <img src={deleteIcon} alt="delete icon" className="erase-icon"/>
            </div>
          </label>
          <button type="submit" className="text-field-submit">Найти&nbsp;вакансию</button>
        </form>
      </div>
      <div className="jobSearchScreen-item jobSearchScreen-item__content">
        <div className="contentItem contentItem__filters">
          <div className="filterItem filterItem__departments">
            <div className="filterItem-title">Департамент</div>
            <Select
              className="basic-single"
              classNamePrefix="select"
              name=""
              options={departmentList}
              onChange={onHandlerFilterDepartment}
              placeholder="Выбрать департамент"
            />
          </div>
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
                    checked={radioChecked === value}
                    onChange={onHandlerClickRadio}
                  />
                  <label htmlFor={index.toString()}>{value}</label>
                </div>
              ))
            }
          </div>
          <div className="filterItem filterItem__salary">
            <div className="filterItem-title">Зарплата</div>
            <div className="salaryInput-wrapper">
              <div className="text-field-salary text-field-salary__min">
                <input className="text-field-salary-input" type="number" min="0" value={salaryMin} onChange={handleChangeMinSalary} placeholder="min"/>
              </div>
              <div className="text-field-salary text-field-salary__max">
                <input className="text-field-salary-input" type="number" min="0" value={salaryMax} onChange={handleChangeMaxSalary} placeholder="max"/>
              </div>
            </div>
          </div>
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