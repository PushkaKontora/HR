import {useEffect, useLayoutEffect, useRef, useState} from 'react';

import './vacancy-list.scss';
import VacancyCard from '../vacancy-card/vacancy-card';
import Modal from '../../reused-components/modal/modal';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setStateRespondModal} from '../../features/vacancy/vacancy-slice';
import PaginationCustom from '../pagination-custom/paginationCustom';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';
import {SortingVacancyTypes} from '../../const';
import DownLoadIcon from '../../assets/img/job-seach/download.svg';
import EmailPlaneIcon from '../../assets/img/vacancy-card/image_email.png';

function VacancyList() {
  const isOpenRespondModalState = useAppSelector((state) => state.vacancy.isOpenRespondModal);
  //const [isOpenRespondModal, setIsOpenRespondModal] = useState(isOpenRespondModalState);
  const [isOpenRespondModal, setIsOpenRespondModal] = useState(true);
  const [radioChecked, setRadioChecked] = useState(false);
  const vacancies = useAppSelector((state) => state.vacancy.vacancies);
  const vacancyForRespond = useAppSelector((state) => state.vacancy.vacancyByID);
  const user = useAppSelector((state) => state.general.user);
  const dispatch = useAppDispatch();
  const firstUpdate = useRef(true);

  useLayoutEffect(() => {
    if (firstUpdate.current) {
      firstUpdate.current = false;
      return;
    }
  });
  useEffect(() => {
    dispatch(getVacancies());
    console.log('VacancyList');
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
            <img src={EmailPlaneIcon} alt="Email Plane Icon"/>
          </div>
          <div className="respondModalItem respondModalItem__content">
            <div className="title">Отправить отклик на вакансию</div>
            <div className="content">
              <div className="itemContent">
                <div className="titleItem">
                  Вакансия
                </div>
                {vacancyForRespond && (
                  <div className="contentItem">
                    {vacancyForRespond?.name}
                  </div>
                )}
              </div>
              <div className="itemContent">
                <div className="titleItem">
                  Резюме
                </div>
                {user?.resume && (
                  <div className="contentItem">
                    {user?.resume.id}
                  </div>
                )}

                <div className="contentItem contentItem__image-addNew">
                  <img src={DownLoadIcon} alt="download icon"/>
                </div>
              </div>
              <div className="itemContent radio-wrapper radio-wrapper__square">
                <label htmlFor='withoutResume'>Отправить без резюме</label>
                <input
                  className="radioInput radioInput__square"
                  type="checkbox"
                  name="respond"
                  id='withoutResume'
                  checked={radioChecked}
                  onChange={onHandlerClickRadio}
                />
              </div>
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

//todo: доделать формат выводимого файла (резюме)