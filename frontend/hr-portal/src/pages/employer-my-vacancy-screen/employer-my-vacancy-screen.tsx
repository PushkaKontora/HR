import {useEffect, useState} from 'react';

import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {ButtonVacancyCard, TabInHeader} from '../../const';
import bannerSearchScreen from '../../assets/img/job-seach/banner-jobSearchPage.svg';
import {setIsGetVacanciesEmployer} from '../../features/vacancy/vacancy-slice';
import VacancyListEmployerMyVacancy from '../../components/vacancy-list-employer-my-vacancy/vacancy-list-employer-my-vacancy';
import './employer-my-vacancy-screen.scss';
import {changeActiveTabInHeader, changeButtonVacancyCard} from '../../features/page/page-slice';


function EmployerMyVacancyScreen() {
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(changeActiveTabInHeader(TabInHeader.myVacancy));
    dispatch(changeButtonVacancyCard(ButtonVacancyCard.empMyVacancy));
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