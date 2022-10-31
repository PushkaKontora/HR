import {ChangeEvent, FormEvent, useEffect, useState} from 'react';
import bannerSearchScreen from '../../assets/img/job-seach/banner-jobSearchPage.svg';
import deleteIcon from '../../assets/img/job-seach/delete-icon.svg';
import './job-search-screen.scss';
import VacancyList from '../../components/vacancy-list/vacancy-list';

const radioInput = ['Любой', 'Более года', 'Более 3 лет', 'Более 6 лет', 'Без опыта'];
const departments = ['SEO', 'frontend', 'backend', 'аналитика'];

enum SelectFilterCard {
  DEFAULT = 'По умолчанию',
  ON_DATE = 'По дате',
  DECREASE_SALARY = 'По убыванию зарплаты',
  INCREASE_SALARY = 'По возрастанию зарплаты'
}

const selectFilterCardVariants = [SelectFilterCard.DEFAULT, SelectFilterCard.ON_DATE, SelectFilterCard.DECREASE_SALARY, SelectFilterCard.INCREASE_SALARY];

function JobSearchScreen() {
  const [pageSearch, setPageSearch] = useState('');
  const [radioChecked, setRadioChecked] = useState(radioInput[0]);
  const [selectDepartment, setSelectDepartment] = useState([]);
  const [salaryMin, setSalaryMin] = useState('');
  const [salaryMax, setSalaryMax] = useState('');
  const [selectFilterCard, setSelectFilterCard] = useState(SelectFilterCard.DEFAULT);
  const [isOpenFilterCard, setIsOpenFilterCard] = useState(false);

  useEffect(() => {
    const parent = document.getElementById('parent');
    const child = document.getElementById('child');

    const cWidth = child?.offsetWidth;
    const pWidth = parent?.offsetWidth;
    if (cWidth && pWidth) {
      cWidth > pWidth ? child.style.width = cWidth + 'px' : child.style.width = pWidth + 'px';
      child.style.width = cWidth + 'px';
    }
  },);


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

  const onToggleSelect = () => {
    setIsOpenFilterCard(!isOpenFilterCard);
  };

  // const onHandleFilterDepartment = (e: ChangeEvent<HTMLInputElement>) => {
  //   setSelectDepartment(e.target.value);
  //   console.log(e.target.value);
  // };

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
          <div className="filterItem">
            <div className="filterItem-title">Департамент</div>
            {/*<select value={selectDepartment} placeholder="Все департаменты" multiple>*/}
            {/*  {*/}
            {/*    departments.map((department, index) => (*/}
            {/*      <option key={index} value={department}>{department}</option>*/}
            {/*    ))*/}
            {/*  }*/}
            {/*</select>*/}
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
            <div className="variantsSorted">
              <button id="parent" onClick={onToggleSelect} className={isOpenFilterCard ? 'variantSorted-select-btn variantSorted-select-btn__active' : 'variantSorted-select-btn'}>{selectFilterCard}</button>
              {isOpenFilterCard && (
                <div id="child" className="variantSorted-option-wrapper">
                  <ul>
                    {
                      selectFilterCardVariants.map((element) => {
                        return (
                          selectFilterCard !== element &&
                          <li onClick={() => setSelectFilterCard(element)} className="variantSorted-element">
                            {element}
                          </li>
                        );
                      })
                    }
                  </ul>
                </div>
              )}
            </div>
          </div>
          <VacancyList/>
        </div>
      </div>
    </div>
  );
}

export default JobSearchScreen;