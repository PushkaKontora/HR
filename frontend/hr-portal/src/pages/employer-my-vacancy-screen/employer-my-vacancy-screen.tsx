import {useEffect, useState} from 'react';

import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {ButtonVacancyCard, TabInHeader} from '../../const';
import bannerMyVacancyScreen from '../../assets/img/header/bunner-my-vacancy.svg';
import {setIsGetVacanciesEmployer} from '../../features/vacancy/vacancy-slice';
import VacancyListEmployerMyVacancy from '../../components/vacancy-list-employer-my-vacancy/vacancy-list-employer-my-vacancy';
import './employer-my-vacancy-screen.scss';
import {changeActiveTabInHeader, changeButtonVacancyCard} from '../../features/page/page-slice';
import {BlueButton} from '../../components/styled/buttons/blue-button';
import {GrayButton} from '../../components/styled/buttons/gray-button';


function EmployerMyVacancyScreen() {
  const stateMyVacancyPublish = useAppSelector((state) => state.vacancy.isPublishedVacancy);
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
        <img src={bannerMyVacancyScreen} alt="banner search screen" className="bannerSearchScreen"/>
      </div>
      <div className="tab-state-my-vacancy">
        {stateMyVacancyPublish
          ? (
            <>
              <BlueButton as="button" width="293px">Активные вакансии</BlueButton>
              <GrayButton as="button" width="293px">Нективные вакансии</GrayButton>
            </>
          ) : (
            <>
              <GrayButton as="button" width="293px">Активные вакансии</GrayButton>
              <BlueButton as="button" width="293px">Нективные вакансии</BlueButton>
            </>
          )
        }
      </div>
      <VacancyListEmployerMyVacancy/>
    </div>
  );
}

export default EmployerMyVacancyScreen;