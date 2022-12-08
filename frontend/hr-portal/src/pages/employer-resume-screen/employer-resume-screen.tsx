import bannerResumeScreen from '../../assets/img/resume-page/resume-page-banner.svg';

import './employer-resume-screen.scss';
import {useEffect} from 'react';
import {useAppDispatch} from '../../app/hooks';
import {changeActiveTabInHeader} from '../../features/page/page-slice';
import {TabInHeader} from '../../const';
import ResumeSearchField from '../../components/resume-search-field/resume-search-field';
import ContentResumeScreen from '../../components/content-resume-screen/content-resume-screen';

function EmployerResumeScreen() {
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(changeActiveTabInHeader(TabInHeader.resume));
  }, []);

  return (
    <div className="employerResumeScree-wrapper">
      <div className="jobSearchScreen-item jobSearchScreen-item__banner">
        <img src={bannerResumeScreen} alt="banner search screen" className="bannerSearchScreen"/>
      </div>
      <div className="search-item">
        <ResumeSearchField/>
      </div>
      <ContentResumeScreen/>
    </div>
  );
}

export default EmployerResumeScreen;