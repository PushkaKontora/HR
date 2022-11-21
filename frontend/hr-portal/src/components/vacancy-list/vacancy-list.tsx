import {useEffect, useLayoutEffect, useRef} from 'react';

import './vacancy-list.scss';
import VacancyCard from '../vacancy-card/vacancy-card';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import PaginationCustom from '../pagination-custom/paginationCustom';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';
import ModalRespondRequest from '../modal-respond-request/modal-respond-request';

function VacancyList() {
  const vacancies = useAppSelector((state) => state.vacancy.vacancies);
  const firstUpdate = useRef(true);
  const dispatch = useAppDispatch();

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

  return (
    <>
      <ModalRespondRequest/>
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