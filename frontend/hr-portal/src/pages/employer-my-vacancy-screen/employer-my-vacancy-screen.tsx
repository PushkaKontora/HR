import {useEffect, useState} from 'react';

import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {TabInHeader} from '../../const';
import {changeActiveTabInHeader} from '../../features/user/user-slice';
import bannerSearchScreen from '../../assets/img/job-seach/banner-jobSearchPage.svg';
import {getVacanciesForEmployer} from '../../service/async-actions/async-actions-vacancy';
import VacancyList from '../../components/vacancy-list/vacancy-list';
import {setIsGetVacanciesEmployer} from '../../features/vacancy/vacancy-slice';

function EmployerMyVacancyScreen() {
  const dispatch = useAppDispatch();
  const departmentId = useAppSelector((state) => state.general?.user?.department.id);
  const isPublished = useAppSelector((state) => state.vacancy.isPublishedVacancy);
  const offset = useAppSelector((state) => state.vacancy.paramsForGetVacancies.offset);

  useEffect(() => {
    if (departmentId) {
      dispatch(getVacanciesForEmployer({isPublished, idDepartment: departmentId, offset}));
    }
  }, [isPublished]);

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
      <VacancyList/>
    </div>
  );
}

export default EmployerMyVacancyScreen;