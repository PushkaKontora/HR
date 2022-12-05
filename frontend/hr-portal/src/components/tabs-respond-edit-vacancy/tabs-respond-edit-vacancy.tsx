import React from 'react';
import likesIcon from '../../assets/img/vacancy-card/yes_like.svg';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {UserStatus} from '../../types/user-status';
import {setIsOpenEditVacancyModal, setTypeRequestModalVacancy, setVacancyByID} from '../../features/vacancy/vacancy-slice';
import {TypeRequestVacancyModal} from '../../const';

function TabsRespondEditVacancy() {
  const vacancyByID = useAppSelector((state) => state.vacancy.vacancyByID);
  const user = useAppSelector((state) => state.general.user);
  const dispatch = useAppDispatch();

  const handlerClickEditVacancy = (e: any) => {
    dispatch(setVacancyByID(vacancyByID));
    e.stopPropagation();
    dispatch(setTypeRequestModalVacancy(TypeRequestVacancyModal.CHANGE));
    dispatch(setIsOpenEditVacancyModal(true));
  };

  if (user?.permission === UserStatus.user) {
    return (
      <div className="navTabs">
        <button className="navTabs-btnItem navTabs-btnItem__respond">
          Откликнуться
        </button>
        <button className="navTabs-btnItem">
          <img src={likesIcon} alt="likes icon"/>
        </button>
      </div>
    );
  }


  if (user?.permission === UserStatus.employer && vacancyByID !== null) {
    return (
      <>
        {
          vacancyByID.department.id === user?.department.id
            ? (
              <div className="navTabs">
                <button className="navTabs-btnItem navTabs-btnItem__respond" onClick={handlerClickEditVacancy}>
                  Редактировать
                </button>
              </div>)
            : (
              <div className="navTabs">
                <button className="navTabs-btnItem navTabs-btnItem__respond">
                  Откликнуться
                </button>
                <button className="navTabs-btnItem">
                  <img src={likesIcon} alt="likes icon"/>
                </button>
              </div>
            )
        }
      </>
    );
  }

  return (<></>);
}

export default TabsRespondEditVacancy;