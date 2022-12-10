import VacancyCard from '../vacancy-card/vacancy-card';
import {useEffect, useLayoutEffect, useRef, useState} from 'react';

import './vacancy-list.scss';
import PaginationCustom from '../pagination-custom/paginationCustom';
import {
  getVacancies,
  getVacancyWishlist,
  VacancyWishListSortBy
} from '../../service/async-actions/async-actions-vacancy';
import ModalRespondRequest from '../modal-respond-request/modal-respond-request';
import {Vacancy} from '../../types/vacancy';
import {useAppDispatch, useAppSelector} from '../../app/hooks';

type VacancyListProps = {
  vacancies: Vacancy[],
  showPagination: boolean
}

function VacancyList(props: VacancyListProps) {
  const firstUpdate = useRef(true);
  const vacancies = useAppSelector((state) => state.vacancy.vacancies);
  const dispatch = useAppDispatch();

  useLayoutEffect(() => {
    if (firstUpdate.current) {
      firstUpdate.current = false;
      dispatch(getVacancyWishlist(VacancyWishListSortBy.added_at_desc));
      return;
    }
  });

  return (
    <>
      <ModalRespondRequest/>
      <div className="vacancyListWrapper">
        <div className="vacancyListItem vacancyListItem__list">
          {
            props.vacancies.map((vacancy) => {
              return (<VacancyCard key={vacancy.id} vacancy={vacancy}/>);
            })
          }
        </div>
        {props.showPagination && <PaginationCustom itemList={vacancies.items}/>}
      </div>
    </>
  );
}

export default VacancyList;