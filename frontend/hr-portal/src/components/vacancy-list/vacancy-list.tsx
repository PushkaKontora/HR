import {useEffect, useState} from 'react';

import './vacancy-list.scss';
import {Vacancies} from '../../mocks/vacancies';
import VacancyCard from '../vacancy-card/vacancy-card';
import Modal from '../../reused-components/modal/modal';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setStateRespondModal} from '../../features/vacancy/vacancy-slice';
import PaginationCustom from '../pagination-custom/paginationCustom';

function VacancyList() {
  const isOpenRespondModalState = useAppSelector((state) => state.vacancy.isOpenRespondModal);
  const [isOpenRespondModal, setIsOpenRespondModal] = useState(isOpenRespondModalState);
  const dispatch = useAppDispatch();

  useEffect(() => {
    setIsOpenRespondModal(isOpenRespondModalState);
  }, [isOpenRespondModalState]);

  useEffect(() => {
    dispatch(setStateRespondModal(isOpenRespondModal));
  }, [isOpenRespondModal]);


  return (
    <>
      <Modal active={isOpenRespondModal} setActive={setIsOpenRespondModal}>
        fvsfvdv
      </Modal>
      <div className="vacancyListWrapper">
        <div className="vacancyListItem vacancyListItem__list">
          {
            Vacancies.map((vacancy) => {
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