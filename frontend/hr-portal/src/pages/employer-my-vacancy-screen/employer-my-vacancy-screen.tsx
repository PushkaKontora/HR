import {useEffect} from 'react';

import {useAppDispatch} from '../../app/hooks';
import {ButtonVacancyCard, TabInHeader, TypeRequestVacancyModal} from '../../const';
import bannerMyVacancyScreen from '../../assets/img/header/bunner-my-vacancy.svg';
import {setIsGetVacanciesEmployer, setIsOpenCreateVacancyModal,  setTypeRequestModalVacancy, setVacancyByID} from '../../features/vacancy/vacancy-slice';
import VacancyListEmployerMyVacancy from '../../components/vacancy-list-employer-my-vacancy/vacancy-list-employer-my-vacancy';
import './employer-my-vacancy-screen.scss';
import {changeActiveTabInHeader, changeButtonVacancyCard} from '../../features/page/page-slice';
import PlusIcon from '../../assets/img/my-vacancy-page/plus-icon.svg';
import TabStateMyVacancy from '../../components/tab-state-my-vacancy/tab-state-my-vacancy';


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

  const handlerClickCreateVacancy = (e: any) => {
    e.stopPropagation();
    dispatch(setIsOpenCreateVacancyModal(true));
    dispatch(setTypeRequestModalVacancy(TypeRequestVacancyModal.CREATE));
  };

  return (
    <div className="employerMyVacancyScreen-wrapper">
      <div className="jobSearchScreen-item jobSearchScreen-item__banner">
        <img src={bannerMyVacancyScreen} alt="banner search screen" className="bannerSearchScreen"/>
      </div>
      <div className="header-action">
        <TabStateMyVacancy/>
        <button className="create-new-vacancy-btn" onClick={handlerClickCreateVacancy}>
          <img src={PlusIcon} alt="icon plus"/>
          <div className="text-btn">Создать вакансию</div>
        </button>
      </div>
      <VacancyListEmployerMyVacancy/>
    </div>
  );
}

export default EmployerMyVacancyScreen;