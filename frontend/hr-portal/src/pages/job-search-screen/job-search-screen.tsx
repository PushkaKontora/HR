import {useEffect} from 'react';

import bannerSearchScreen from '../../assets/img/job-seach/banner-jobSearchPage.svg';
import './job-search-screen.scss';
import {useAppDispatch} from '../../app/hooks';
import {getDepartment} from '../../service/async-actions/async-actions-vacancy';
import VacancyContent from '../../components/vacancy-content/vacancy-content';


function JobSearchScreen() {
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(getDepartment());
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