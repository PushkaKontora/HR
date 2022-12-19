import bannerResumeScreen from '../../assets/img/resume-page/resume-page-banner.svg';

import './employer-resume-screen.scss';
import {useEffect} from 'react';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {changeActiveTabInHeader} from '../../features/page/page-slice';
import {TabInHeader, TypeActionPagination} from '../../const';
import ResumeSearchField from '../../components/resume-search-field/resume-search-field';
import ContentResumeScreen from '../../components/content-resume-screen/content-resume-screen';
import {getCompetenciesAction} from '../../service/async-actions/async-actions-competencies';
import {getResumeList, getResumeWishlist, ResumeWishListSortBy} from '../../service/async-actions/async-actions-resume';
import {setTypeActionPagination} from '../../features/vacancy/vacancy-slice';
import {getVacancyWishlist, VacancyWishListSortBy} from '../../service/async-actions/async-actions-vacancy';
import {UserStatus} from '../../types/user-status';

function EmployerResumeScreen() {
  const user = useAppSelector((state) => state.general.user);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(changeActiveTabInHeader(TabInHeader.resume));
    dispatch(getCompetenciesAction());
    dispatch(getResumeList());
    dispatch(setTypeActionPagination(TypeActionPagination.RESUME_EMPLOYER));

    dispatch(getVacancyWishlist(VacancyWishListSortBy.added_at_desc));

    if (user?.permission === UserStatus.employer) {
      dispatch(getResumeWishlist(ResumeWishListSortBy.added_at_desc));
    }
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