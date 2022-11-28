import {useEffect} from 'react';

import bannerSearchScreen from '../../assets/img/job-seach/banner-jobSearchPage.svg';
import './job-search-screen.scss';
import {useAppDispatch} from '../../app/hooks';
import {getDepartment} from '../../service/async-actions/async-actions-vacancy';
import VacancyContent from '../../components/vacancy-content/vacancy-content';
import {changeButtonVacancyCard} from '../../features/page/page-slice';
import {ButtonVacancyCard} from '../../const';


function JobSearchScreen() {
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(getDepartment());
    dispatch(changeButtonVacancyCard(ButtonVacancyCard.vacancies));
  }, []);

  return (
    <div className="jobSearchScreen-wrapper">
      <div className="jobSearchScreen-item jobSearchScreen-item__banner">
        <img src={bannerSearchScreen} alt="banner search screen" className="bannerSearchScreen"/>
      </div>
      <VacancyContent/>
    </div>
  );
}

export default JobSearchScreen;