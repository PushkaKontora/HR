import {useEffect, useState} from 'react';

import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {TabInHeader} from '../../const';
import {changeActiveTabInHeader} from '../../features/user/user-slice';
import bannerSearchScreen from '../../assets/img/job-seach/banner-jobSearchPage.svg';
import {setIsGetVacanciesEmployer} from '../../features/vacancy/vacancy-slice';
import VacancyListVacanciesPage from '../../components/vacancy-list-vacancies-page/vacancy-list-vacancies-page';
import VacancyListEmployerMyVacancy from '../../components/vacancy-list-employer-my-vacancy/vacancy-list-employer-my-vacancy';

function EmployerMyVacancyScreen() {
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(changeActiveTabInHeader(TabInHeader.myVacancy));
    dispatch(setIsGetVacanciesEmployer(true));
    return () => {
      dispatch(setIsGetVacanciesEmployer(false));
    };
  }, []);

  return (
    <div className="employerMyVacancyScreen-wrapper">
      <div className="jobSearchScreen-item jobSearchScreen-item__banner">
        <img src={bannerSearchScreen} alt="banner search screen" className="bannerSearchScreen"/>
      </div>
      <VacancyListEmployerMyVacancy/>
    </div>
  );
}

export default EmployerMyVacancyScreen;