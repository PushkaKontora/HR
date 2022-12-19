import {useEffect} from 'react';

import bannerSearchScreen from '../../assets/img/job-seach/banner-jobSearchPage.svg';
import './job-search-screen.scss';
import {useAppDispatch} from '../../app/hooks';
import {getDepartment} from '../../service/async-actions/async-actions-vacancy';
import VacancyContent from '../../components/vacancy-content/vacancy-content';
import {changeActiveTabInHeader, changeButtonVacancyCard} from '../../features/page/page-slice';
import {ButtonVacancyCard, TabInHeader, TypeActionPagination} from '../../const';
import {setIsPublishedVacancy, setTypeActionPagination} from '../../features/vacancy/vacancy-slice';
import ModalMakeUnpublishVacancy from '../../components/modal-make-unpublish-vacancy/modal-make-unpublish-vacancy';
import ModalEditVacancy from '../../components/modal-edit-vacancy/modal-edit-vacancy';


function JobSearchScreen() {
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(getDepartment());
    dispatch(changeButtonVacancyCard(ButtonVacancyCard.vacancies));
    dispatch(changeActiveTabInHeader(TabInHeader.vacancies));
    dispatch(setTypeActionPagination(TypeActionPagination.VACANCY));
    dispatch(setIsPublishedVacancy(true));
  }, []);

  return (
    <>
      <ModalEditVacancy/>
      <ModalMakeUnpublishVacancy/>
      <div className="jobSearchScreen-wrapper">
        <div className="jobSearchScreen-item jobSearchScreen-item__banner">
          <img src={bannerSearchScreen} alt="banner search screen" className="bannerSearchScreen"/>
        </div>
        <VacancyContent/>
      </div>
    </>
  );
}

export default JobSearchScreen;