import { useEffect, useState} from 'react';

import './vacancy-list.scss';
import VacancyCard from '../vacancy-card/vacancy-card';
import Modal from '../../reused-components/modal/modal';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setStateRespondModal} from '../../features/vacancy/vacancy-slice';
import PaginationCustom from '../pagination-custom/paginationCustom';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';
import {SortingVacancyTypes} from '../../const';
import DownLoadIcon from '../../assets/img/job-seach/download.svg';

function VacancyList() {
  const isOpenRespondModalState = useAppSelector((state) => state.vacancy.isOpenRespondModal);
  const [isOpenRespondModal, setIsOpenRespondModal] = useState(isOpenRespondModalState);
  //const [isOpenRespondModal, setIsOpenRespondModal] = useState(true);
  const [radioChecked, setRadioChecked] = useState(false);
  const vacancies = useAppSelector((state) => state.vacancy.vacancies);
  const vacancyForRespond = useAppSelector((state) => state.vacancy.vacancyByID);
  const user = useAppSelector((state) => state.general.user);
  const dispatch = useAppDispatch();

  const dataState = useAppSelector((state) => state.vacancy.paramsForGetVacancies);
  const departmentListShort = useAppSelector((state) => state.vacancy.departmentsShortVersions);


  useEffect(() => {
    dispatch(getVacancies({dataState, departmentListShort}));
  }, []);

  useEffect(() => {
    setIsOpenRespondModal(isOpenRespondModalState);
  }, [isOpenRespondModalState]);

  useEffect(() => {
    dispatch(setStateRespondModal(isOpenRespondModal));
  }, [isOpenRespondModal]);

  const onHandlerClickRadio = (e: any) => {
    e.stopPropagation();
    setRadioChecked(!radioChecked);
  };

  return (
    <>
      <Modal
        padding="80px"
        width={1178}
        active={isOpenRespondModal}
        setActive={setIsOpenRespondModal}
      >
        <div className="respondModalWrapper">
          <div className="respondModalItem respondModalItem__img">
            <img src="" alt=""/>
          </div>
          <div className="respondModalItem respondModalItem__content">
            <div className="title">Отправить отклик на вакансию</div>
            <div className="content">
              {/*<div className="itemContent">*/}
              {/*  <div className="titleItem">*/}
              {/*    Вакансия*/}
              {/*  </div>*/}
              {/*  <div className="contentItem">*/}
              {/*    {vacancyForRespond?.name}*/}
              {/*  </div>*/}
              {/*</div>*/}
              {/*<div className="itemContent">*/}
              {/*  <div className="titleItem">*/}
              {/*    Резюме*/}
              {/*  </div>*/}
              {/*  <div className="contentItem">*/}
              {/*    {user?.resume.id}*/}
              {/*  </div>*/}
              {/*  <div className="contentItem">*/}
              {/*    <img src={DownLoadIcon} alt="download icon"/>*/}
              {/*  </div>*/}
              {/*</div>*/}
              {/*<div className="itemContent radio-wrapper radio-wrapper__square">*/}
              {/*  <input*/}
              {/*    className="radioInput radioInput__square"*/}
              {/*    type="checkbox"*/}
              {/*    name="respond"*/}
              {/*    id='withoutResume'*/}
              {/*    checked={radioChecked}*/}
              {/*    onClick={onHandlerClickRadio}*/}
              {/*  />*/}
              {/*  <label htmlFor='withoutResume'>Отправить без резюме</label>*/}
              {/*</div>*/}
            </div>
            <div className="btn-wrapper">
              <button className="btn-sendRespond">Отправить отклик</button>
            </div>
          </div>
        </div>
      </Modal>
      <div className="vacancyListWrapper">
        <div className="vacancyListItem vacancyListItem__list">
          {
            vacancies.items.map((vacancy) => {
              return (<VacancyCard key={vacancy.id} vacancy={vacancy}/>);
            })
          }
        </div>
        <PaginationCustom/>
      </div>
    </>
  );
}

export default VacancyList;

//todo: сделать модалку на отклик