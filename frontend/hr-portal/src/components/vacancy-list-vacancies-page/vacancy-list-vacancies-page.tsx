import {useEffect, useLayoutEffect, useRef} from 'react';

import './vacancy-list-vacancies-page.scss';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';
import ModalRespondRequest from '../modal-respond-request/modal-respond-request';
import VacancyList from '../vacancy-list/vacancy-list';

function VacancyListVacanciesPage() {
  const firstUpdate = useRef(true);
  const dispatch = useAppDispatch();
  const vacancies = useAppSelector((state) => state.vacancy.vacancies);

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
      <VacancyList showPagination={true} vacancies={vacancies.items}/>
    </>
  );
}

export default VacancyListVacanciesPage;

//todo: доделать формат выводимого файла (резюме)