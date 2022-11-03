import {ChangeEvent, FormEvent, useEffect, useState} from 'react';
import bannerSearchScreen from '../../assets/img/job-seach/banner-jobSearchPage.svg';
import deleteIcon from '../../assets/img/job-seach/delete-icon.svg';
import './job-search-screen.scss';
import VacancyList from '../../components/vacancy-list/vacancy-list';
import CardSorting from '../../components/card-sorting/card-sorting';
import Select from 'react-select';

const radioInput = ['Любой', 'Более года', 'Более 3 лет', 'Более 6 лет', 'Без опыта'];
const departments = [
  {
    'value': 1,
    'label': 'SEO'
  }, {
    'value': 11,
    'label': 'frontend'
  }, {
    'value': 5,
    'label': 'backend'
  }, {
    'value': 3,
    'label': 'аналитика'
  },
  {
    'value': 111,
    'label': 'frontend'
  }, {
    'value': 455,
    'label': 'backend'
  }, {
    'value': 543,
    'label': 'аналитика'
  },{
    'value': 661,
    'label': 'SEO'
  }, {
    'value': 1661,
    'label': 'frontend'
  }, {
    'value': 6665,
    'label': 'backend'
  }, {
    'value': 3646,
    'label': 'аналитика'
  },
  {
    'value': 11661,
    'label': 'frontend'
  }, {
    'value': 45455,
    'label': 'backend'
  }, {
    'value': 54453,
    'label': 'аналитика'
  },
];


function JobSearchScreen() {
  const [pageSearch, setPageSearch] = useState('');
  const [radioChecked, setRadioChecked] = useState(radioInput[0]);
  const [selectDepartment, setSelectDepartment] = useState<null | string | undefined>(null);
  const [salaryMin, setSalaryMin] = useState('');
  const [salaryMax, setSalaryMax] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setPageSearch(e.target.value);
  };

  const handleChangeMinSalary = (e: ChangeEvent<HTMLInputElement>) => {
    setSalaryMin(e.target.value);
  };

  const handleChangeMaxSalary = (e: ChangeEvent<HTMLInputElement>) => {
    setSalaryMax(e.target.value);
  };

  const handleEraseSearch = () => {
    setPageSearch('');
  };

  const onHandleClickRadio = (e: ChangeEvent<HTMLInputElement>) => {
    setRadioChecked(e.target.value);
  };

  const onHandleFilterDepartment = (e: any) => {
    setSelectDepartment(e.target.value);
    console.log(e.target.value);
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
              options={departments}
              onChange={(e) => setSelectDepartment(e?.label)}
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
                    onChange={onHandleClickRadio}
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
          <div className="filterItem">
            <div className="filterItem-title">Сбросить фильтр</div>
          </div>
        </div>
        <div className="contentItem contentItem__vacancies">
          <div className="cardVacancy-title">
            <div className="title">Найдена 131 вакансия</div>
            <CardSorting/>
          </div>
          <VacancyList/>
        </div>
      </div>
    </div>
  );
}

export default JobSearchScreen;