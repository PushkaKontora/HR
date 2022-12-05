import {useEffect, useLayoutEffect, useRef} from 'react';

import './vacancy-list-vacancies-page.scss';
import VacancyCard from '../vacancy-card/vacancy-card';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import PaginationCustom from '../pagination-custom/paginationCustom';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';
import ModalRespondRequest from '../modal-respond-request/modal-respond-request';
import VacancyList from '../vacancy-list/vacancy-list';

function VacancyListVacanciesPage() {
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
  }, []);

  return (
    <>
      <ModalRespondRequest/>
      <VacancyList/>
    </>
  );
}

export default VacancyListVacanciesPage;

//todo: доделать формат выводимого файла (резюме)