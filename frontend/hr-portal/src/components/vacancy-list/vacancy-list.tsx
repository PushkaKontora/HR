import {useEffect, useState} from 'react';

import './vacancy-list.scss';
import VacancyCard from '../vacancy-card/vacancy-card';
import Modal from '../../reused-components/modal/modal';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setStateRespondModal} from '../../features/vacancy/vacancy-slice';
import PaginationCustom from '../pagination-custom/paginationCustom';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';
import {SortingVacancyTypes} from '../../const';

function VacancyList() {
  const isOpenRespondModalState = useAppSelector((state) => state.vacancy.isOpenRespondModal);
  const [isOpenRespondModal, setIsOpenRespondModal] = useState(isOpenRespondModalState);
  const vacancies = useAppSelector((state) => state.vacancy.vacancies);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(getVacancies({sortBy: SortingVacancyTypes.BY_NAME, offset: 0}));
  }, []);

  useEffect(() => {
    setIsOpenRespondModal(isOpenRespondModalState);
  }, [isOpenRespondModalState]);

  useEffect(() => {
    dispatch(setStateRespondModal(isOpenRespondModal));
  }, [isOpenRespondModal]);


  return (
    <>
      <Modal
        padding="80px"
        width={1236}
        active={isOpenRespondModal}
        setActive={setIsOpenRespondModal}
      >
        <div className="respondModalWrapper">
          <div className="respondModalItem respondModalItem__img">

          </div>
          <div className="respondModalItem respondModalItem__content">
            <div className="title">Отправить отклик на вакансию</div>
            <div className="content"/>
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